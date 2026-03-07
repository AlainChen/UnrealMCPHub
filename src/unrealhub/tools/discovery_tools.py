import asyncio
import logging
from urllib.parse import urlparse

from mcp.server.fastmcp import FastMCP

from unrealhub.ue_client import UEMCPClient
from unrealhub.utils.process import find_unreal_editor_processes

logger = logging.getLogger(__name__)


def register_discovery_tools(mcp: FastMCP, get_config, get_state) -> None:
    @mcp.tool()
    async def discover_instances(rescan: bool = False) -> str:
        """List known UE MCP instances, optionally scanning for new ones.

        rescan: If True, actively scans configured ports for running UE MCP endpoints.
                If False, lists instances from stored state (fast).

        Discovered instances are auto-registered and assigned aliases (ue1, ue2, ...).
        """
        state = get_state()

        if rescan:
            config = get_config()
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

        summary = state.list_instances_summary()
        return summary or "No instances registered. Run discover_instances(rescan=True) first."

    @mcp.tool()
    async def manage_instance(
        action: str,
        instance: str = "",
        url: str = "",
        port: int = 0,
        alias: str = "",
    ) -> str:
        """Manage UE MCP instances: register, unregister, set alias, or switch active.

        action: 'register', 'unregister', 'set_alias', or 'use'.
        instance: Instance ID or alias (required for unregister / set_alias / use).
        url: MCP endpoint URL (required for register, e.g. 'http://localhost:8422/mcp').
        port: Port number for register (auto-extracted from URL if 0).
        alias: Custom alias (required for set_alias, e.g. 'MyGame').
        """
        state = get_state()

        if action == "register":
            if not url:
                return "url is required for 'register' action."
            if not port:
                try:
                    parsed = urlparse(url)
                    port = parsed.port or 8422
                except Exception:
                    port = 8422
            inst = state.register_instance(url=url, port=port)
            state.save()
            return f"Registered instance: {inst.auto_id} at {url}"

        if action == "unregister":
            if not instance:
                return "instance is required for 'unregister' action."
            if state.unregister_instance(instance):
                state.save()
                return f"Instance '{instance}' removed."
            return f"Instance '{instance}' not found."

        if action == "set_alias":
            if not instance or not alias:
                return "instance and alias are required for 'set_alias' action."
            if state.set_alias(instance, alias):
                state.save()
                return f"Alias '{alias}' set for instance '{instance}'."
            return f"Instance '{instance}' not found."

        if action == "use":
            if not instance:
                return "instance is required for 'use' action."
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

        return f"Unknown action '{action}'. Use 'register', 'unregister', 'set_alias', or 'use'."
