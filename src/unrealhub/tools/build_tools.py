from __future__ import annotations

import asyncio
import logging
import re
import time
from typing import Any

from mcp.server.fastmcp import FastMCP, Context

from unrealhub.utils.ue_paths import UEPathResolver

logger = logging.getLogger(__name__)

_UBT_PROGRESS_RE = re.compile(r"\[(\d+)/(\d+)\]")


def _analyze_build_output(output: str) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    for line in output.splitlines():
        ll = line.lower()
        if "error" in ll and (
            "error c" in ll or "error lnk" in ll or ": error" in ll
        ):
            errors.append(line.strip())
        elif "warning" in ll and (
            "warning c" in ll or ": warning" in ll
        ):
            warnings.append(line.strip())
    return {
        "errors": errors,
        "warnings": warnings,
        "error_count": len(errors),
        "warning_count": len(warnings),
    }


async def _stream_process(
    process: asyncio.subprocess.Process,
    ctx: Context | None,
    timeout: float,
) -> tuple[str, int]:
    """Read subprocess stdout line-by-line, sending progress & log notifications.

    Every non-empty line is forwarded to the client immediately:
    - ``[x/y]`` lines → ``report_progress`` + ``ctx.info``
    - error lines → ``ctx.error``
    - warning lines → ``ctx.warning``
    - everything else → ``ctx.info``

    Returns (full_output, exit_code).  Raises asyncio.TimeoutError on timeout.
    """
    assert process.stdout is not None
    lines: list[str] = []
    deadline = asyncio.get_event_loop().time() + timeout

    async def _read_lines() -> None:
        async for raw in process.stdout:  # type: ignore[union-attr]
            line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
            lines.append(line)

            if ctx is None:
                continue

            stripped = line.rstrip()
            if not stripped:
                continue

            ll = line.lower()

            m = _UBT_PROGRESS_RE.search(line)
            if m:
                cur, total = int(m.group(1)), int(m.group(2))
                await ctx.report_progress(cur, total, stripped)
                await ctx.info(stripped)
            elif "error" in ll:
                await ctx.error(stripped)
            elif "warning" in ll:
                await ctx.warning(stripped)
            else:
                await ctx.info(stripped)

    remaining = deadline - asyncio.get_event_loop().time()
    await asyncio.wait_for(_read_lines(), timeout=max(remaining, 0))

    remaining = deadline - asyncio.get_event_loop().time()
    await asyncio.wait_for(process.wait(), timeout=max(remaining, 0))

    return "\n".join(lines), process.returncode or 0


def register_build_tools(mcp: FastMCP, get_config, get_state) -> None:
    @mcp.tool()
    async def build_project(
        action: str = "compile",
        target: str = "Editor",
        configuration: str = "Development",
        platform: str = "Win64",
        extra_args: str = "",
        ctx: Context | None = None,
    ) -> str:
        """Build the UE project (streams progress in real time).

        action: 'compile' (UBT compile) or 'cook' (RunUAT BuildCookRun).
        target: Build target suffix, compile only (Editor, Game, Client, Server). Default 'Editor'.
        configuration: Development, Shipping, DebugGame, etc. Compile only.
        platform: Win64, Linux, etc.
        extra_args: Additional arguments passed to UBT or RunUAT.

        Requires project to be configured via setup_project first.
        Progress notifications are streamed to the client during the build.
        """
        config = get_config()
        project = config.get_active_project()
        if not project:
            return (
                "No project configured. Call setup_project() first with your "
                ".uproject path."
            )

        try:
            paths = UEPathResolver.resolve_from_uproject(
                project.uproject_path, project.engine_root
            )
        except ValueError as e:
            return f"Path resolution failed: {e}"

        if action == "compile":
            return await _compile(
                paths, target, configuration, platform, extra_args, ctx=ctx
            )
        if action == "cook":
            return await _cook(paths, platform, extra_args, ctx=ctx)
        return f"Unknown action '{action}'. Use 'compile' or 'cook'."


async def _compile(
    paths,
    target,
    configuration,
    platform,
    extra_args,
    build_target_override=None,
    *,
    ctx: Context | None = None,
) -> str:
    success, exit_code, output, analysis = await _run_compile(
        paths, target, configuration, platform, extra_args, build_target_override,
        ctx=ctx,
    )

    if exit_code is None or analysis is None:
        return output

    result_lines = [
        f"Build {'SUCCEEDED' if success else 'FAILED'}",
        f"Exit code: {exit_code}",
        f"Target: {(build_target_override or f'{paths.project_name}{target}')} {platform} {configuration}",
        f"Errors: {analysis['error_count']}, "
        f"Warnings: {analysis['warning_count']}",
        "",
    ]

    if analysis["errors"]:
        result_lines.append("=== ERRORS ===")
        for err in analysis["errors"][:20]:
            result_lines.append(err)
        result_lines.append("")

    if analysis["warnings"]:
        result_lines.append("=== WARNINGS ===")
        for warn in analysis["warnings"][:10]:
            result_lines.append(warn)
        result_lines.append("")

    output_lines = output.strip().split("\n")
    tail = output_lines[-50:] if len(output_lines) > 50 else output_lines
    result_lines.append("=== BUILD OUTPUT (tail) ===")
    result_lines.extend(tail)

    return "\n".join(result_lines)


async def _run_compile(
    paths,
    target,
    configuration,
    platform,
    extra_args,
    build_target_override=None,
    *,
    ctx: Context | None = None,
):
    project_name = paths.project_name
    build_target = build_target_override or f"{project_name}{target}"

    cmd: list[str] = [
        paths.build_bat,
        build_target,
        platform,
        configuration,
        paths.uproject_path,
        "-waitmutex",
    ]
    if extra_args:
        cmd.extend(extra_args.split())

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        output, exit_code = await _stream_process(process, ctx, timeout=600)

        analysis = _analyze_build_output(output)
        return exit_code == 0, exit_code, output, analysis

    except asyncio.TimeoutError:
        return False, None, "Build timed out after 600 seconds.", None
    except FileNotFoundError:
        return False, None, f"Build.bat not found at: {paths.build_bat}", None
    except Exception as e:
        logger.exception("compile failed")
        return False, None, f"Build failed with exception: {e}", None


async def _cook(
    paths,
    platform,
    extra_args,
    *,
    ctx: Context | None = None,
) -> str:
    cmd: list[str] = [
        paths.uat_bat,
        "BuildCookRun",
        f"-project={paths.uproject_path}",
        f"-platform={platform}",
        "-nocompile",
        "-cook",
    ]
    if extra_args:
        cmd.extend(extra_args.split())

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        output, exit_code = await _stream_process(process, ctx, timeout=1800)

        analysis = _analyze_build_output(output)

        result_lines = [
            f"Cook {'SUCCEEDED' if exit_code == 0 else 'FAILED'}",
            f"Exit code: {exit_code}",
            f"Platform: {platform}",
            f"Errors: {analysis['error_count']}, "
            f"Warnings: {analysis['warning_count']}",
            "",
        ]

        if analysis["errors"]:
            result_lines.append("=== ERRORS ===")
            for err in analysis["errors"][:20]:
                result_lines.append(err)
            result_lines.append("")

        output_lines = output.strip().split("\n")
        tail = output_lines[-50:] if len(output_lines) > 50 else output_lines
        result_lines.append("=== OUTPUT (tail) ===")
        result_lines.extend(tail)

        return "\n".join(result_lines)

    except asyncio.TimeoutError:
        return "Cook timed out after 1800 seconds."
    except FileNotFoundError:
        return f"RunUAT.bat not found at: {paths.uat_bat}"
    except Exception as e:
        logger.exception("cook failed")
        return f"Cook failed with exception: {e}"
