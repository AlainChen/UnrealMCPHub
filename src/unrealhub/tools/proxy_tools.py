import json
import logging
import time
from typing import Any

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)


def register_proxy_tools(mcp: FastMCP, get_state, get_client) -> None:
    """
    get_state: callable returning StateStore
    get_client: callable(instance_id: str | None) -> UEMCPClient | None
        If instance_id is None, returns client for active instance.
    """

    def _offline_message() -> str:
        state = get_state()
        summary = state.list_instances_summary()
        active = state.get_active_instance()
        if active and active.status == "crashed":
            return (
                f"UE instance '{active.auto_id}' has CRASHED.\n"
                f"Use get_log(source='crash') for details, or launch_editor(action='restart') to restart.\n"
                f"\n{summary}"
            )
        return (
            f"No active UE instance online.\n"
            f"Use launch_editor() to start the editor, or discover_instances() to find running ones.\n"
            f"\n{summary}"
        )

    def _format_tool_result(result: dict[str, Any]) -> str:
        if not result.get("success", False):
            return f"[UE Tool Error] {result.get('error', 'Unknown error')}"

        content = result.get("content")
        if not isinstance(content, list):
            return str(content) if content is not None else "(empty result)"

        parts: list[str] = []
        for item in content:
            if not isinstance(item, dict):
                parts.append(str(item))
                continue
            ctype = item.get("type", "")
            if ctype == "text":
                parts.append(item.get("text", ""))
            elif ctype == "image":
                mime = item.get("mimeType") or item.get("mime_type", "unknown")
                data = item.get("data")
                if isinstance(data, str):
                    size = len(data)
                    parts.append(f"[Image: {mime}, {size} chars base64]")
                else:
                    parts.append(f"[Image: {mime}]")
            else:
                if "repr" in item:
                    parts.append(item["repr"])
                elif "text" in item:
                    parts.append(item["text"])
                else:
                    parts.append(str(item))

        return "\n".join(parts) if parts else "(empty result)"

    @mcp.tool()
    async def ue_status() -> str:
        """Get the status of the current active UE instance.
        Shows: online/offline/crashed, PID, port, project path."""
        state = get_state()
        active = state.get_active_instance()
        if not active:
            return "No active instance.\n" + (
                state.list_instances_summary() or "No instances registered. Run discover_instances()."
            )

        lines = [
            f"Active instance: {active.auto_id}"
            + (f" ({active.alias})" if active.alias else ""),
            f"Status: {active.status}",
            f"URL: {active.url}",
            f"PID: {active.pid or 'unknown'}",
            f"Project: {active.project_path or 'unknown'}",
            f"Crashes: {active.crash_count}",
            f"Last seen: {active.last_seen}",
        ]
        return "\n".join(lines)

    @mcp.tool()
    async def ue_list_tools(domain: str = "") -> str:
        """List available tools from the active UE instance.

        domain: If empty, lists all MCP-level tools with parameter schemas.
                If specified, queries the dispatch system for tools in that domain.

        Use this to discover available tools before calling ue_call().
        """
        client = get_client(None)
        if not client:
            return _offline_message()

        if domain:
            result = await client.call_tool("get_dispatch", {"domain": domain})
            return _format_tool_result(result)

        state = get_state()
        active = state.get_active_instance()

        try:
            tools = await client.list_tools()
        except Exception as e:
            return f"Failed to fetch tools: {e}"

        if not tools:
            return "No tools returned from UE instance."

        inst_id = active.auto_id if active else "unknown"
        lines = [f"UE Instance '{inst_id}' has {len(tools)} tool(s):\n"]
        for t in tools:
            lines.append(f"### {t.get('name', '?')}")
            if t.get("description"):
                lines.append(f"  {t['description'][:200]}")
            schema = t.get("inputSchema", {})
            props = schema.get("properties", {})
            if props:
                required = set(schema.get("required", []))
                params = []
                for pname, pinfo in props.items():
                    ptype = pinfo.get("type", "any")
                    req = " (required)" if pname in required else ""
                    desc = pinfo.get("description", "")
                    params.append(
                        f"    {pname}: {ptype}{req}"
                        + (f" - {desc[:80]}" if desc else "")
                    )
                lines.append("  Parameters:")
                lines.extend(params)
            lines.append("")

        return "\n".join(lines)

    @mcp.tool()
    async def ue_call(
        tool_name: str, arguments: dict | None = None, domain: str = ""
    ) -> str:
        """Call a tool on the active UE instance.

        tool_name: Name of the tool (e.g. 'search_console_commands').
        arguments: Tool arguments as a dict (e.g. {"keyword": "stat"}).
        domain: If specified, calls via the dispatch system (e.g. 'level', 'blueprint').
                If empty, calls the tool directly.

        Use ue_list_tools() first to see available tools and their parameter schemas.
        """
        client = get_client(None)
        if not client:
            return _offline_message()

        state = get_state()
        active = state.get_active_instance()
        start = time.time()

        if domain:
            result = await client.call_tool(
                "call_dispatch_tool",
                {
                    "domain": domain,
                    "tool_name": tool_name,
                    "arguments": json.dumps(arguments) if arguments else "{}",
                },
            )
            log_name = f"{domain}/{tool_name}"
        else:
            result = await client.call_tool(tool_name, arguments or {})
            log_name = tool_name

        duration = (time.time() - start) * 1000

        if active:
            state.record_tool_call(active.auto_id, log_name, result["success"], duration)
            state.save()

        return _format_tool_result(result)

    @mcp.tool()
    async def ue_run_python(script: str) -> str:
        """Execute a Python script in the UE Editor. The 'result' variable will be returned.
        Operates on the active instance (switch with manage_instance(action='use'))."""
        client = get_client(None)
        if not client:
            return _offline_message()

        state = get_state()
        active = state.get_active_instance()

        start = time.time()
        result = await client.call_tool("run_python_script", {"script": script})
        duration = (time.time() - start) * 1000

        if active:
            state.record_tool_call(
                active.auto_id, "run_python_script", result["success"], duration
            )
            state.save()

        return _format_tool_result(result)

