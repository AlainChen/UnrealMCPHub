import asyncio
import logging
import os
from typing import Any

from mcp.server.fastmcp import FastMCP

from unrealhub.utils.ue_paths import UEPathResolver

logger = logging.getLogger(__name__)


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


def register_build_tools(mcp: FastMCP, get_config, get_state) -> None:
    @mcp.tool()
    async def build_project(
        action: str = "compile",
        target: str = "Editor",
        configuration: str = "Development",
        platform: str = "Win64",
        extra_args: str = "",
    ) -> str:
        """Build the UE project.

        action: 'compile' (UBT compile) or 'cook' (RunUAT BuildCookRun).
        target: Build target suffix, compile only (Editor, Game, Client, Server). Default 'Editor'.
        configuration: Development, Shipping, DebugGame, etc. Compile only.
        platform: Win64, Linux, etc.
        extra_args: Additional arguments passed to UBT or RunUAT.

        Requires project to be configured via setup_project first.
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
            return await _compile(paths, target, configuration, platform, extra_args)
        if action == "cook":
            return await _cook(paths, platform, extra_args)
        return f"Unknown action '{action}'. Use 'compile' or 'cook'."


async def _compile(paths, target, configuration, platform, extra_args) -> str:
    project_name = paths.project_name
    build_target = f"{project_name}{target}"

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

        stdout_data, _ = await asyncio.wait_for(
            process.communicate(),
            timeout=600,
        )
        output = stdout_data.decode("utf-8", errors="replace")
        exit_code = process.returncode or 0

        analysis = _analyze_build_output(output)

        result_lines = [
            f"Build {'SUCCEEDED' if exit_code == 0 else 'FAILED'}",
            f"Exit code: {exit_code}",
            f"Target: {build_target} {platform} {configuration}",
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

    except asyncio.TimeoutError:
        return "Build timed out after 600 seconds."
    except FileNotFoundError:
        return f"Build.bat not found at: {paths.build_bat}"
    except Exception as e:
        logger.exception("compile failed")
        return f"Build failed with exception: {e}"


async def _cook(paths, platform, extra_args) -> str:
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

        stdout_data, _ = await asyncio.wait_for(
            process.communicate(),
            timeout=1800,
        )
        output = stdout_data.decode("utf-8", errors="replace")
        exit_code = process.returncode or 0

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
