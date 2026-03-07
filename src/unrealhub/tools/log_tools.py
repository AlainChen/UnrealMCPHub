import logging
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from unrealhub.tools.build_tools import _analyze_build_output
from unrealhub.utils.ue_paths import UEPathResolver

logger = logging.getLogger(__name__)


def register_log_tools(mcp: FastMCP, get_config, get_state) -> None:
    @mcp.tool()
    async def get_log(
        source: str = "editor",
        instance: str = "",
        tail_lines: int = 100,
    ) -> str:
        """Read diagnostic logs.

        source: 'editor' (UE Editor log), 'build' (UBT build log), or 'crash' (crash reports).
        instance: Instance ID (for editor/crash, defaults to active).
        tail_lines: Number of lines to show (default 100). For build log, controls tail bytes via tail_lines * 2560.
        """
        if source == "editor":
            return await _log_editor(get_state, instance, tail_lines)
        if source == "build":
            return _log_build(tail_lines)
        if source == "crash":
            return _log_crash(get_state, instance)
        return f"Unknown source '{source}'. Use 'editor', 'build', or 'crash'."


async def _log_editor(get_state, instance: str, tail_lines: int) -> str:
    state = get_state()
    inst = state.get_active_instance() if not instance else state.get_instance(instance)
    if not inst or not inst.project_path:
        return "No instance with known project path."

    log_dir = Path(inst.project_path).parent / "Saved" / "Logs"
    if not log_dir.exists():
        return f"Log directory not found: {log_dir}"

    log_files = sorted(log_dir.glob("*.log"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not log_files:
        return "No log files found."

    log_file = log_files[0]
    try:
        with open(log_file, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        tail = lines[-tail_lines:] if len(lines) > tail_lines else lines
        return f"Log: {log_file.name} ({len(lines)} lines)\n{''.join(tail)}"
    except Exception as e:
        return f"Error reading log: {e}"


def _log_build(tail_lines: int) -> str:
    log_path = UEPathResolver.get_ubt_log_path()
    json_log_path = UEPathResolver.get_ubt_log_json_path()

    if not os.path.exists(log_path):
        return f"Build log not found at: {log_path}"

    tail_bytes = tail_lines * 2560
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
        f"Errors: {analysis['error_count']}, Warnings: {analysis['warning_count']}",
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
    tail_display = output_lines[-80:] if len(output_lines) > 80 else output_lines
    result_lines.extend(tail_display)

    if os.path.exists(json_log_path):
        result_lines.append("")
        result_lines.append(f"JSON log available at: {json_log_path}")

    return "\n".join(result_lines)


def _log_crash(get_state, instance: str) -> str:
    state = get_state()
    inst = state.get_active_instance() if not instance else state.get_instance(instance)
    if not inst or not inst.project_path:
        return "No instance with known project path."

    from datetime import datetime
    from unrealhub.utils.process import find_crash_dirs

    project_dir = str(Path(inst.project_path).parent)
    crashes = find_crash_dirs(project_dir)

    if not crashes:
        return "No crash reports found."

    lines = [f"Found {len(crashes)} crash report(s):"]
    for crash in crashes[:5]:
        mtime_str = datetime.fromtimestamp(crash["modified_time"]).isoformat()
        lines.append(f"\n--- {crash['name']} ({mtime_str}) ---")
        crash_dir = Path(crash["dir_path"])
        for fname in ["CrashContext.runtime-xml", "Diagnostics.txt", "minidump.dmp"]:
            fpath = crash_dir / fname
            if fpath.exists():
                if fname.endswith(".dmp"):
                    lines.append(f"  {fname}: {fpath.stat().st_size} bytes")
                else:
                    try:
                        content = fpath.read_text(encoding="utf-8", errors="replace")[:2000]
                        lines.append(f"  {fname}:\n{content}")
                    except Exception:
                        lines.append(f"  {fname}: (could not read)")

    return "\n".join(lines)
