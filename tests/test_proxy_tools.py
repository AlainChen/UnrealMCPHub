"""Test the helper functions in proxy_tools (format and offline logic)."""
import json
from unittest.mock import MagicMock, AsyncMock, patch

import pytest

from unrealhub.state import StateStore


def _make_proxy_module():
    """Import register_proxy_tools and construct its internal helpers for testing."""
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("test")

    store = MagicMock(spec=StateStore)
    store.list_instances_summary.return_value = "  ue1 (ue1): online *"
    store.get_active_instance.return_value = None

    get_client = MagicMock(return_value=None)

    from unrealhub.tools.proxy_tools import register_proxy_tools
    register_proxy_tools(mcp, lambda: store, get_client)

    return mcp, store, get_client


class TestFormatToolResult:
    """Test _format_tool_result indirectly through ue_call."""

    @pytest.mark.asyncio
    async def test_offline_message(self, tmp_home):
        mcp, store, get_client = _make_proxy_module()
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        assert "ue_status" in tools

    @pytest.mark.asyncio
    async def test_ue_call_invalid_json(self, tmp_home):
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP("test")

        active = MagicMock()
        active.auto_id = "ue1"
        active.status = "online"
        active.alias = None
        active.url = "http://localhost:8422/mcp"
        active.pid = 1234
        active.project_path = "/test"
        active.crash_count = 0
        active.last_seen = "now"

        store = MagicMock(spec=StateStore)
        store.get_active_instance.return_value = active

        mock_client = MagicMock()
        get_client = MagicMock(return_value=mock_client)

        from unrealhub.tools.proxy_tools import register_proxy_tools
        register_proxy_tools(mcp, lambda: store, get_client)

        tools = {t.name: t.fn for t in mcp._tool_manager.list_tools()}
        result = await tools["ue_call"]("test_tool", "NOT_JSON")
        assert "Invalid JSON" in result


class TestProxyFormatting:
    """Test formatting of proxy tool results by calling internal formatting via ue_call."""

    @pytest.mark.asyncio
    async def test_format_success_text(self, tmp_home):
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP("test")

        active = MagicMock()
        active.auto_id = "ue1"
        active.status = "online"

        store = MagicMock(spec=StateStore)
        store.get_active_instance.return_value = active

        mock_client = AsyncMock()
        mock_client.call_tool = AsyncMock(return_value={
            "success": True,
            "content": [{"type": "text", "text": "hello world"}],
            "error": None,
        })
        get_client = MagicMock(return_value=mock_client)

        from unrealhub.tools.proxy_tools import register_proxy_tools
        register_proxy_tools(mcp, lambda: store, get_client)

        tools = {t.name: t.fn for t in mcp._tool_manager.list_tools()}
        result = await tools["ue_call"]("some_tool", "{}")
        assert "hello world" in result

    @pytest.mark.asyncio
    async def test_format_error(self, tmp_home):
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP("test")

        active = MagicMock()
        active.auto_id = "ue1"
        active.status = "online"

        store = MagicMock(spec=StateStore)
        store.get_active_instance.return_value = active

        mock_client = AsyncMock()
        mock_client.call_tool = AsyncMock(return_value={
            "success": False,
            "content": [],
            "error": "Something broke",
        })
        get_client = MagicMock(return_value=mock_client)

        from unrealhub.tools.proxy_tools import register_proxy_tools
        register_proxy_tools(mcp, lambda: store, get_client)

        tools = {t.name: t.fn for t in mcp._tool_manager.list_tools()}
        result = await tools["ue_call"]("bad_tool", "{}")
        assert "Something broke" in result

    @pytest.mark.asyncio
    async def test_format_image(self, tmp_home):
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP("test")

        active = MagicMock()
        active.auto_id = "ue1"
        active.status = "online"

        store = MagicMock(spec=StateStore)
        store.get_active_instance.return_value = active

        mock_client = AsyncMock()
        mock_client.call_tool = AsyncMock(return_value={
            "success": True,
            "content": [{"type": "image", "mimeType": "image/png", "data": "abc123"}],
            "error": None,
        })
        get_client = MagicMock(return_value=mock_client)

        from unrealhub.tools.proxy_tools import register_proxy_tools
        register_proxy_tools(mcp, lambda: store, get_client)

        tools = {t.name: t.fn for t in mcp._tool_manager.list_tools()}
        result = await tools["ue_call"]("img_tool", "{}")
        assert "Image" in result
        assert "image/png" in result
