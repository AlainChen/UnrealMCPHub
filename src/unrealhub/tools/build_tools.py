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
    async def compile_project(
        target: str = "Editor",
        configuration: str = "Development",
        platform: str = "Win64",
        extra_args: str = "",
    ) -> str:
        """Compile the UE project using UnrealBuildTool.

        target: Build target suffix (Editor, Game, Client, Server). Default 'Editor'.
        configuration: Development, Shipping, DebugGame, etc.
        platform: Win64, Linux, etc.
        extra_args: Additional UBT arguments (e.g. '-waitmutex').

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
            logger.exception("compile_project failed")
            return f"Build failed with exception: {e}"

    @mcp.tool()
    async def get_build_log(tail_bytes: int = 256000) -> str:
        """Read and analyze the latest UBT build log.

        Returns error/warning summary and log tail.
        """
        log_path = UEPathResolver.get_ubt_log_path()
        json_log_path = UEPathResolver.get_ubt_log_json_path()

        if not os.path.exists(log_path):
            return f"Build log not found at: {log_path}"

        try:
            size = os.path.getsize(log_path)
            read_from = max(0, size - tail_bytes)
            with open(log_path, "rb") as f:
                f.seek(read_from)
                tail_data = f.read()
            tail_text = tail_data.decode("utf-8", errors="replace")
        except OSError as e:
            return f"Failed to read log: {e}"

        analysis = _analyze_build_output(tail_text)

        result_lines = [
            f"Log: {log_path}",
            f"Size: {size} bytes, showing last {len(tail_data)} bytes",
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

        result_lines.append("=== LOG TAIL ===")
        output_lines = tail_text.strip().split("\n")
        tail_lines = output_lines[-80:] if len(output_lines) > 80 else output_lines
        result_lines.extend(tail_lines)

        if os.path.exists(json_log_path):
            result_lines.append("")
            result_lines.append(f"JSON log available at: {json_log_path}")

        return "\n".join(result_lines)

    @mcp.tool()
    async def cook_project(
        platform: str = "Win64",
        extra_args: str = "",
    ) -> str:
        """Cook/package the project using RunUAT.

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
            logger.exception("cook_project failed")
            return f"Cook failed with exception: {e}"
