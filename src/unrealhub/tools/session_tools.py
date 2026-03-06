import logging

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)


def register_session_tools(mcp: FastMCP, get_state) -> None:
    @mcp.tool()
    async def add_note(content: str, instance: str = "") -> str:
        """Add a note to an instance (or active instance).
        Useful for recording observations, crash reasons, or context for crash recovery."""
        state = get_state()
        inst = state.get_active_instance() if not instance else state.get_instance(instance)
        if not inst:
            return "No instance found."
        state.add_note(inst.auto_id, content)
        state.save()
        return f"Note added to {inst.auto_id}: {(content[:100] + '...') if len(content) > 100 else content}"

    @mcp.tool()
    async def get_notes(instance: str = "") -> str:
        """Get all notes for an instance."""
        state = get_state()
        inst = state.get_active_instance() if not instance else state.get_instance(instance)
        if not inst:
            return "No instance found."
        notes = state.get_notes(inst.auto_id)
        if not notes:
            return f"No notes for {inst.auto_id}."
        lines = [f"Notes for {inst.auto_id} ({len(notes)}):"]
        for n in notes:
            lines.append(f"  [{n.timestamp}] {n.content}")
        return "\n".join(lines)

    @mcp.tool()
    async def get_call_history(instance: str = "", limit: int = 30) -> str:
        """Get recent tool call history for an instance."""
        state = get_state()
        inst = state.get_active_instance() if not instance else state.get_instance(instance)
        if not inst:
            return "No instance found."
        history = state.get_call_history(inst.auto_id, limit=limit)
        if not history:
            return f"No call history for {inst.auto_id}."
        lines = [f"Call history for {inst.auto_id} (last {len(history)}):"]
        for h in history:
            status = "OK" if h.success else "FAIL"
            lines.append(f"  [{h.timestamp}] {h.tool_name} -> {status} ({h.duration_ms:.0f}ms)")
        return "\n".join(lines)

    @mcp.tool()
    async def export_session(instance: str = "", format: str = "text") -> str:
        """Export session data for an instance.
        format: 'text' or 'json'"""
        state = get_state()
        inst = state.get_active_instance() if not instance else state.get_instance(instance)
        if not inst:
            return "No instance found."

        if format == "json":
            return inst.model_dump_json(indent=2)

        lines = [
            f"=== Session Export: {inst.auto_id} ===",
            f"URL: {inst.url}",
            f"Status: {inst.status}",
            f"Project: {inst.project_path}",
            f"Crashes: {inst.crash_count}",
            f"First seen: {inst.first_seen}",
            f"Last seen: {inst.last_seen}",
            "",
            f"--- Notes ({len(inst.notes)}) ---",
        ]
        for n in inst.notes:
            lines.append(f"[{n.timestamp}] {n.content}")

        lines.append(f"\n--- Call History ({len(inst.call_history)}) ---")
        for h in inst.call_history[-50:]:
            status = "OK" if h.success else "FAIL"
            lines.append(f"[{h.timestamp}] {h.tool_name} -> {status}")

        return "\n".join(lines)
