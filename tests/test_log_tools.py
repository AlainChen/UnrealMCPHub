"""Test log_tools (get_log with source=editor|build|crash)."""
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from mcp.server.fastmcp import FastMCP
from unrealhub.state import StateStore
from unrealhub.tools.log_tools import register_log_tools


def _setup(tmp_home):
    mcp = FastMCP("test")
    config = MagicMock()
    store = StateStore()
    store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=1234)
    register_log_tools(mcp, lambda: config, lambda: store)
    tools = {t.name: t.fn for t in mcp._tool_manager.list_tools()}
    return store, config, tools


class TestGetLogEditor:
    @pytest.mark.asyncio
    async def test_no_instance(self, tmp_home):
        mcp = FastMCP("test")
        store = StateStore()
        register_log_tools(mcp, lambda: MagicMock(), lambda: store)
        tools = {t.name: t.fn for t in mcp._tool_manager.list_tools()}
        result = await tools["get_log"]("editor")
        assert "no instance" in result.lower()

    @pytest.mark.asyncio
    async def test_no_log_dir(self, tmp_home, tmp_path):
        store, _, tools = _setup(tmp_home)
        inst = store.get_active_instance()
        inst.project_path = str(tmp_path / "Fake" / "Fake.uproject")
        result = await tools["get_log"]("editor")
        assert "not found" in result.lower()

    @pytest.mark.asyncio
    async def test_reads_log_file(self, tmp_home, tmp_path):
        store, _, tools = _setup(tmp_home)
        proj = tmp_path / "MyProj"
        log_dir = proj / "Saved" / "Logs"
        log_dir.mkdir(parents=True)
        log_file = log_dir / "MyProj.log"
        log_file.write_text("Line 1\nLine 2\nLine 3\n", encoding="utf-8")

        inst = store.get_active_instance()
        inst.project_path = str(proj / "MyProj.uproject")
        result = await tools["get_log"]("editor")
        assert "Line 1" in result
        assert "3 lines" in result


class TestGetLogBuild:
    @pytest.mark.asyncio
    async def test_no_log_file(self, tmp_home):
        store, _, tools = _setup(tmp_home)
        with patch(
            "unrealhub.tools.log_tools.UEPathResolver.get_ubt_log_path",
            return_value="C:/nonexistent/log.txt",
        ):
            result = await tools["get_log"]("build")
        assert "not found" in result.lower()

    @pytest.mark.asyncio
    async def test_reads_build_log(self, tmp_home, tmp_path):
        store, _, tools = _setup(tmp_home)
        log_file = tmp_path / "build.log"
        content = "file.cpp(1): error C2065: undeclared\nBuilding...\nDone.\n"
        log_file.write_text(content, encoding="utf-8")

        with patch(
            "unrealhub.tools.log_tools.UEPathResolver.get_ubt_log_path",
            return_value=str(log_file),
        ), patch(
            "unrealhub.tools.log_tools.UEPathResolver.get_ubt_log_json_path",
            return_value=str(tmp_path / "nope.json"),
        ):
            result = await tools["get_log"]("build")
        assert "Errors: 1" in result
        assert "C2065" in result


class TestGetLogCrash:
    @pytest.mark.asyncio
    async def test_no_instance(self, tmp_home):
        mcp = FastMCP("test")
        store = StateStore()
        register_log_tools(mcp, lambda: MagicMock(), lambda: store)
        tools = {t.name: t.fn for t in mcp._tool_manager.list_tools()}
        result = await tools["get_log"]("crash")
        assert "no instance" in result.lower()

    @pytest.mark.asyncio
    async def test_no_crash_reports(self, tmp_home, tmp_path):
        store, _, tools = _setup(tmp_home)
        proj_dir = tmp_path / "Proj"
        proj_dir.mkdir()
        inst = store.get_active_instance()
        inst.project_path = str(proj_dir / "Proj.uproject")

        with patch(
            "unrealhub.utils.process.find_crash_dirs", return_value=[]
        ):
            result = await tools["get_log"]("crash")
        assert "no crash" in result.lower()


class TestGetLogUnknownSource:
    @pytest.mark.asyncio
    async def test_unknown_source(self, tmp_home):
        store, _, tools = _setup(tmp_home)
        result = await tools["get_log"]("invalid")
        assert "unknown source" in result.lower()


class TestOnlyGetLogRegistered:
    def test_single_tool(self, tmp_home):
        _, _, tools = _setup(tmp_home)
        assert set(tools.keys()) == {"get_log"}
