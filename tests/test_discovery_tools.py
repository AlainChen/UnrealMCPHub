"""Test discovery_tools (discover_instances, manage_instance)."""
from unittest.mock import MagicMock

import pytest

from mcp.server.fastmcp import FastMCP
from unrealhub.state import StateStore
from unrealhub.tools.discovery_tools import register_discovery_tools


def _setup(tmp_home):
    mcp = FastMCP("test")
    config = MagicMock()
    config.get_scan_ports.return_value = [8422, 8423]
    store = StateStore()
    register_discovery_tools(mcp, lambda: config, lambda: store)
    tools = {t.name: t.fn for t in mcp._tool_manager.list_tools()}
    return store, config, tools


class TestToolRegistration:
    def test_only_two_tools(self, tmp_home):
        _, _, tools = _setup(tmp_home)
        assert set(tools.keys()) == {"discover_instances", "manage_instance"}

    def test_removed_tools(self, tmp_home):
        _, _, tools = _setup(tmp_home)
        for removed in ("list_instances", "use_editor"):
            assert removed not in tools


class TestDiscoverInstancesNoRescan:
    @pytest.mark.asyncio
    async def test_empty_state(self, tmp_home):
        _, _, tools = _setup(tmp_home)
        result = await tools["discover_instances"]()
        assert "no instances" in result.lower()

    @pytest.mark.asyncio
    async def test_lists_known(self, tmp_home):
        store, _, tools = _setup(tmp_home)
        store.register_instance(url="http://localhost:8422/mcp", port=8422, pid=100)
        result = await tools["discover_instances"]()
        assert "ue1" in result


class TestManageInstanceRegister:
    @pytest.mark.asyncio
    async def test_register(self, tmp_home):
        store, _, tools = _setup(tmp_home)
        result = await tools["manage_instance"]("register", url="http://localhost:9999/mcp")
        assert "registered" in result.lower()
        assert len(store.list_instances()) == 1

    @pytest.mark.asyncio
    async def test_register_no_url(self, tmp_home):
        _, _, tools = _setup(tmp_home)
        result = await tools["manage_instance"]("register")
        assert "url is required" in result.lower()


class TestManageInstanceUnregister:
    @pytest.mark.asyncio
    async def test_unregister(self, tmp_home):
        store, _, tools = _setup(tmp_home)
        store.register_instance(url="http://localhost:8422/mcp", port=8422)
        result = await tools["manage_instance"]("unregister", instance="ue1")
        assert "removed" in result.lower()

    @pytest.mark.asyncio
    async def test_unregister_not_found(self, tmp_home):
        _, _, tools = _setup(tmp_home)
        result = await tools["manage_instance"]("unregister", instance="ghost")
        assert "not found" in result.lower()


class TestManageInstanceSetAlias:
    @pytest.mark.asyncio
    async def test_set_alias(self, tmp_home):
        store, _, tools = _setup(tmp_home)
        store.register_instance(url="http://localhost:8422/mcp", port=8422)
        result = await tools["manage_instance"]("set_alias", instance="ue1", alias="MyGame")
        assert "MyGame" in result


class TestManageInstanceUse:
    @pytest.mark.asyncio
    async def test_use(self, tmp_home):
        store, _, tools = _setup(tmp_home)
        store.register_instance(url="http://localhost:8422/mcp", port=8422)
        store.register_instance(url="http://localhost:8423/mcp", port=8423)
        result = await tools["manage_instance"]("use", instance="ue2")
        assert "switched" in result.lower()
        assert store.get_active_instance().auto_id == "ue2"

    @pytest.mark.asyncio
    async def test_use_not_found(self, tmp_home):
        _, _, tools = _setup(tmp_home)
        result = await tools["manage_instance"]("use", instance="ghost")
        assert "not found" in result.lower()

    @pytest.mark.asyncio
    async def test_use_no_instance(self, tmp_home):
        _, _, tools = _setup(tmp_home)
        result = await tools["manage_instance"]("use")
        assert "instance is required" in result.lower()


class TestManageInstanceUnknownAction:
    @pytest.mark.asyncio
    async def test_unknown(self, tmp_home):
        _, _, tools = _setup(tmp_home)
        result = await tools["manage_instance"]("fly")
        assert "unknown action" in result.lower()
