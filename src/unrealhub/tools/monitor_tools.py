import logging
from pathlib import Path

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)


def register_monitor_tools(mcp: FastMCP, get_state, get_watcher) -> None:
    """get_watcher returns ProcessWatcher instance."""

    @mcp.tool()
    async def get_instance_health(instance: str = "") -> str:
        """Get detailed health status of a UE instance.
        If instance is empty, uses active instance."""
        state = get_state()
        if not instance:
            inst = state.get_active_instance()
        else:
            inst = state.get_instance(instance)

        if not inst:
            return "No instance found. Run discover_instances() first."

        from unrealhub.utils.process import get_process_info, is_process_alive
        from unrealhub.ue_client import UEMCPClient

        lines = [
            f"Instance: {inst.auto_id}" + (f" ({inst.alias})" if inst.alias else ""),
            f"URL: {inst.url}",
            f"Status: {inst.status}",
            f"PID: {inst.pid or 'unknown'}",
            f"Project: {inst.project_path or 'unknown'}",
            f"Crash count: {inst.crash_count}",
            f"First seen: {inst.first_seen}",
            f"Last seen: {inst.last_seen}",
            f"Last health check: {inst.last_health_check}",
        ]

        if inst.pid:
            alive = is_process_alive(inst.pid)
            lines.append(f"Process alive: {alive}")
            if alive:
                info = get_process_info(inst.pid)
                if info:
                    lines.append(f"CPU: {info.get('cpu_percent', '?')}%, Memory: {info.get('memory_mb', '?')} MB")

        http_ok = await UEMCPClient.probe_endpoint(inst.url, timeout=2.0)
        lines.append(f"HTTP endpoint: {'responding' if http_ok else 'NOT responding'}")

        return "\n".join(lines)

    @mcp.tool()
    async def get_instance_log(instance: str = "", tail_lines: int = 100) -> str:
        """Read the UE Editor log file for an instance."""
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

    @mcp.tool()
    async def get_crash_report(instance: str = "") -> str:
        """Get crash report details for an instance."""
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

    @mcp.tool()
    async def get_monitor_report() -> str:
        """Get a monitoring summary of all instances."""
        state = get_state()
        instances = state.list_instances()
        if not instances:
            return "No instances registered."

        lines = ["=== Monitor Report ===\n"]
        for inst in instances:
            lines.append(f"[{inst.auto_id}] {inst.status.upper()}" + (f" ({inst.alias})" if inst.alias else ""))
            lines.append(f"  URL: {inst.url}")
            lines.append(f"  Crashes: {inst.crash_count}")
            lines.append(f"  Tool calls: {len(inst.call_history)}")
            lines.append(f"  Notes: {len(inst.notes)}")
            lines.append("")

        return "\n".join(lines)
