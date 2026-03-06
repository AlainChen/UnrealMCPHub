import asyncio
import logging
from urllib.parse import urlparse

from mcp.server.fastmcp import FastMCP

from unrealhub.ue_client import UEMCPClient
from unrealhub.utils.process import find_unreal_editor_processes

logger = logging.getLogger(__name__)


def register_discovery_tools(mcp: FastMCP, get_config, get_state) -> None:
    @mcp.tool()
    async def discover_instances() -> str:
        """Scan configured ports for running UE MCP instances.
        Automatically registers discovered instances and assigns aliases (ue1, ue2, ...)."""
        config = get_config()
        state = get_state()
        ports = config.get_scan_ports()

        results: list[dict] = []

        async def probe_port(port: int) -> None:
            url = f"http://localhost:{port}/mcp"
            if await UEMCPClient.probe_endpoint(url, timeout=2.0):
                results.append({"port": port, "url": url})

        await asyncio.gather(*(probe_port(p) for p in ports))

        if not results:
            return (
                f"No UE MCP instances found on ports {ports}.\n"
                "Is UE Editor running with RemoteMCP enabled?"
            )

        running_procs = find_unreal_editor_processes()
        report_lines: list[str] = []

        for r in results:
            existing = [
                inst for inst in state.list_instances() if inst.port == r["port"]
            ]
            if existing:
                state.update_status(existing[0].auto_id, "online")
                state.save()
                report_lines.append(
                    f"  {existing[0].auto_id} (port {r['port']}): "
                    "already registered, status -> online"
                )
                continue

            project_path = ""
            pid = None
            for proc in running_procs:
                if proc.get("project_path"):
                    project_path = proc["project_path"]
                    pid = proc.get("pid")
                    break

            instance = state.register_instance(
                url=r["url"],
                port=r["port"],
                project_path=project_path,
                pid=pid,
            )
            state.update_status(instance.auto_id, "online", pid=pid)
            report_lines.append(
                f"  {instance.auto_id} (port {r['port']}): NEW, "
                f"project={project_path or 'unknown'}"
            )

        state.save()

        lines = [f"Discovered {len(results)} instance(s):"]
        lines.extend(report_lines)

        active = state.get_active_instance()
        if active:
            lines.append(f"\nActive instance: {active.auto_id}")

        return "\n".join(lines)

    @mcp.tool()
    async def list_instances() -> str:
        """List all known UE MCP instances with their status."""
        state = get_state()
        summary = state.list_instances_summary()
        return summary or "No instances registered. Run discover_instances() first."

    @mcp.tool()
    async def register_instance(url: str, port: int = 0) -> str:
        """Manually register a UE MCP instance by URL.

        url: MCP endpoint URL, e.g. 'http://localhost:8422/mcp'
        port: Port number (auto-extracted from URL if 0)
        """
        state = get_state()

        if not port:
            try:
                parsed = urlparse(url)
                port = parsed.port or 8422
            except Exception:
                port = 8422

        instance = state.register_instance(url=url, port=port)
        state.save()
        return f"Registered instance: {instance.auto_id} at {url}"

    @mcp.tool()
    async def unregister_instance(instance: str) -> str:
        """Remove a registered instance by ID or alias."""
        state = get_state()
        if state.unregister_instance(instance):
            state.save()
            return f"Instance '{instance}' removed."
        return f"Instance '{instance}' not found."

    @mcp.tool()
    async def use_editor(instance: str) -> str:
        """Switch the active UE Editor instance. All subsequent ue_* tools will target this instance.

        instance: Instance identifier - auto alias ('ue1') or custom alias ('MyGame').

        Similar to 'source venv/bin/activate' or 'kubectl config use-context'.
        Single-instance users never need this - the first discovered instance auto-activates.
        """
        state = get_state()
        inst = state.get_instance(instance)
        if not inst:
            available = state.list_instances_summary()
            return f"Instance '{instance}' not found.\n{available}"

        state.set_active(instance)
        state.save()

        alias_part = f" ({inst.alias})" if inst.alias else ""
        return (
            f"Active instance switched to: {inst.auto_id}{alias_part}\n"
            f"URL: {inst.url}, Status: {inst.status}"
        )

    @mcp.tool()
    async def set_instance_alias(instance: str, alias: str) -> str:
        """Set a custom alias for an instance.

        instance: Current identifier (e.g. 'ue1')
        alias: New custom alias (e.g. 'MyGame')
        """
        state = get_state()
        if state.set_alias(instance, alias):
            state.save()
            return f"Alias '{alias}' set for instance '{instance}'."
        return f"Instance '{instance}' not found."
