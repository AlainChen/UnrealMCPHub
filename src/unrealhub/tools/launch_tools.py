import asyncio
import logging
import time

import psutil

from mcp.server.fastmcp import FastMCP

from unrealhub.ue_client import UEMCPClient
from unrealhub.utils.process import find_unreal_editor_processes, is_process_alive
from unrealhub.utils.ue_paths import UEPathResolver

logger = logging.getLogger(__name__)


def register_launch_tools(
    mcp: FastMCP, get_config, get_state, get_ue_client_factory
) -> None:
    @mcp.tool()
    async def launch_editor(
        wait_for_mcp: bool = True,
        timeout: int = 120,
    ) -> str:
        """Launch the UE Editor for the active project and optionally wait for MCP.

        wait_for_mcp: If True, polls until RemoteMCP is responding (default True).
        timeout: Max seconds to wait for MCP readiness.

        Requires project configured via setup_project.
        """
        config = get_config()
        project = config.get_active_project()
        if not project:
            return "No project configured. Call setup_project() first."

        try:
            paths = UEPathResolver.resolve_from_uproject(
                project.uproject_path, project.engine_root
            )
        except ValueError as e:
            return f"Path resolution failed: {e}"

        running = find_unreal_editor_processes()
        project_norm = project.uproject_path.replace("\\", "/").lower()
        for proc in running:
            proc_path = (proc.get("project_path") or "").replace("\\", "/").lower()
            if proc_path == project_norm:
                return (
                    f"Editor already running for this project (PID: {proc['pid']}). "
                    f"MCP port: {project.mcp_port}"
                )

        try:
            process = await asyncio.create_subprocess_exec(
                paths.editor_exe,
                paths.uproject_path,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            editor_pid = process.pid or 0
        except FileNotFoundError:
            return f"Editor not found at: {paths.editor_exe}"
        except Exception as e:
            logger.exception("launch_editor failed")
            return f"Failed to launch editor: {e}"

        state = get_state()

        if not wait_for_mcp:
            return (
                f"Editor launched (PID: {editor_pid}). Not waiting for MCP. "
                "Check status with get_editor_status()."
            )

        mcp_url = f"http://localhost:{project.mcp_port}/mcp"
        start = time.monotonic()

        while (time.monotonic() - start) < timeout:
            if await UEMCPClient.probe_endpoint(mcp_url, timeout=2.0):
                instance = state.register_instance(
                    url=mcp_url,
                    port=project.mcp_port,
                    project_path=project.uproject_path,
                    engine_root=project.engine_root,
                    pid=editor_pid,
                )
                state.update_status(instance.auto_id, "online", pid=editor_pid)
                state.save()
                return (
                    f"Editor launched and MCP ready!\n"
                    f"PID: {editor_pid}\n"
                    f"MCP: {mcp_url}\n"
                    f"Instance: {instance.auto_id}"
                )
            await asyncio.sleep(3)

        return (
            f"Editor launched (PID: {editor_pid}) but MCP did not become ready "
            f"within {timeout}s.\n"
            "Check if RemoteMCP plugin is enabled and MCP.Start has been run."
        )

    @mcp.tool()
    async def restart_editor(timeout: int = 120) -> str:
        """Restart the currently active UE Editor instance.

        Useful after a crash. Launches a new editor and waits for MCP.
        """
        state = get_state()
        active = state.get_active_instance()
        if not active:
            return "No active instance to restart. Use launch_editor() instead."

        if active.pid and is_process_alive(active.pid):
            try:
                proc = psutil.Process(active.pid)
                proc.terminate()
                await asyncio.sleep(2)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        state.update_status(active.auto_id, "starting")
        state.save()

        return await launch_editor(wait_for_mcp=True, timeout=timeout)

    @mcp.tool()
    async def get_editor_status() -> str:
        """Check if UE Editor processes are currently running."""
        procs = find_unreal_editor_processes()
        if not procs:
            return "No UE Editor processes found."

        lines = [f"Found {len(procs)} UE Editor process(es):"]
        for p in procs:
            project_path = p.get("project_path", "unknown")
            lines.append(f"  PID: {p['pid']}, Project: {project_path}")
        return "\n".join(lines)
