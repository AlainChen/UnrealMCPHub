"""Test session_tools (add_note, get_notes, get_call_history, export_session)."""
from unittest.mock import MagicMock

import pytest

from mcp.server.fastmcp import FastMCP
from unrealhub.state import StateStore
from unrealhub.tools.session_tools import register_session_tools


def _setup(tmp_home):
    mcp = FastMCP("test")
    store = StateStore()
    store.register_instance(url="http://localhost:8422/mcp", port=8422, pid=1234)
    register_session_tools(mcp, lambda: store)
    tools = {t.name: t.fn for t in mcp._tool_manager.list_tools()}
    return store, tools


class TestSessionTools:
    @pytest.mark.asyncio
    async def test_add_note(self, tmp_home):
        store, tools = _setup(tmp_home)
        result = await tools["add_note"]("Test observation")
        assert "added" in result.lower()
        notes = store.get_notes("ue1")
        assert len(notes) == 1
        assert notes[0].content == "Test observation"

    @pytest.mark.asyncio
    async def test_get_notes_empty(self, tmp_home):
        store, tools = _setup(tmp_home)
        result = await tools["get_notes"]()
        assert "no notes" in result.lower()

    @pytest.mark.asyncio
    async def test_get_notes_with_content(self, tmp_home):
        store, tools = _setup(tmp_home)
        store.add_note("ue1", "Note 1")
        store.add_note("ue1", "Note 2")
        result = await tools["get_notes"]()
        assert "Note 1" in result
        assert "Note 2" in result

    @pytest.mark.asyncio
    async def test_get_call_history_empty(self, tmp_home):
        store, tools = _setup(tmp_home)
        result = await tools["get_call_history"]()
        assert "no call history" in result.lower()

    @pytest.mark.asyncio
    async def test_get_call_history_with_data(self, tmp_home):
        store, tools = _setup(tmp_home)
        store.record_tool_call("ue1", "run_python", True, 42.0)
        store.record_tool_call("ue1", "get_dispatch", False, 100.0)
        result = await tools["get_call_history"]()
        assert "run_python" in result
        assert "OK" in result
        assert "FAIL" in result

    @pytest.mark.asyncio
    async def test_export_session_text(self, tmp_home):
        store, tools = _setup(tmp_home)
        store.add_note("ue1", "A note")
        store.record_tool_call("ue1", "test", True, 1.0)
        result = await tools["export_session"]()
        assert "Session Export" in result
        assert "A note" in result
        assert "test" in result

    @pytest.mark.asyncio
    async def test_export_session_json(self, tmp_home):
        store, tools = _setup(tmp_home)
        result = await tools["export_session"]("", "json")
        import json
        data = json.loads(result)
        assert data["auto_id"] == "ue1"
        assert "url" in data

    @pytest.mark.asyncio
    async def test_no_instance(self, tmp_home):
        mcp = FastMCP("test")
        store = StateStore()
        register_session_tools(mcp, lambda: store)
        tools = {t.name: t.fn for t in mcp._tool_manager.list_tools()}

        result = await tools["add_note"]("orphan note")
        assert "no instance" in result.lower()

    @pytest.mark.asyncio
    async def test_add_note_truncation(self, tmp_home):
        store, tools = _setup(tmp_home)
        long = "x" * 200
        result = await tools["add_note"](long)
        assert "..." in result
