"""Test build_tools (_analyze_build_output + build_project tool registration)."""
from unittest.mock import MagicMock

import pytest

from mcp.server.fastmcp import FastMCP
from unrealhub.tools.build_tools import _analyze_build_output, register_build_tools


class TestAnalyzeBuildOutput:
    def test_clean_output(self):
        output = "Building...\nDone.\nResult: Succeeded\n"
        result = _analyze_build_output(output)
        assert result["error_count"] == 0
        assert result["warning_count"] == 0

    def test_errors_detected(self):
        output = (
            "file.cpp(42): error C2065: 'x': undeclared identifier\n"
            "file.cpp(50): error C2143: syntax error\n"
            "Building...\n"
        )
        result = _analyze_build_output(output)
        assert result["error_count"] == 2
        assert len(result["errors"]) == 2
        assert "C2065" in result["errors"][0]

    def test_warnings_detected(self):
        output = (
            "file.cpp(10): warning C4267: conversion may lose data\n"
            "file.cpp(20): warning C4996: deprecated\n"
            "Done.\n"
        )
        result = _analyze_build_output(output)
        assert result["warning_count"] == 2
        assert len(result["warnings"]) == 2

    def test_mixed(self):
        output = (
            "file.cpp(1): error C2065: undeclared\n"
            "file.cpp(2): warning C4267: conversion\n"
            "file.cpp(3): error LNK2019: unresolved external\n"
            "Done.\n"
        )
        result = _analyze_build_output(output)
        assert result["error_count"] == 2
        assert result["warning_count"] == 1

    def test_linker_errors(self):
        output = "test.obj : error LNK2019: unresolved external symbol\n"
        result = _analyze_build_output(output)
        assert result["error_count"] == 1

    def test_generic_error_not_matched(self):
        output = "Some error occurred in the build system\n"
        result = _analyze_build_output(output)
        assert result["error_count"] == 0

    def test_empty_output(self):
        result = _analyze_build_output("")
        assert result["error_count"] == 0
        assert result["warning_count"] == 0


class TestBuildProjectRegistration:
    def test_only_build_project_registered(self):
        mcp = FastMCP("test")
        register_build_tools(mcp, MagicMock, MagicMock)
        tools = {t.name for t in mcp._tool_manager.list_tools()}
        assert tools == {"build_project"}

    def test_removed_tools_not_registered(self):
        mcp = FastMCP("test")
        register_build_tools(mcp, MagicMock, MagicMock)
        tool_names = {t.name for t in mcp._tool_manager.list_tools()}
        for removed in ("compile_project", "cook_project", "get_build_log"):
            assert removed not in tool_names


class TestBuildProjectNoConfig:
    @pytest.mark.asyncio
    async def test_no_project(self):
        mcp = FastMCP("test")
        config = MagicMock()
        config.get_active_project.return_value = None
        register_build_tools(mcp, lambda: config, MagicMock)
        tools = {t.name: t.fn for t in mcp._tool_manager.list_tools()}
        result = await tools["build_project"]()
        assert "no project" in result.lower()

    @pytest.mark.asyncio
    async def test_unknown_action(self):
        mcp = FastMCP("test")
        config = MagicMock()
        proj = MagicMock()
        proj.uproject_path = "C:/Fake/Fake.uproject"
        proj.engine_root = "C:/FakeEngine"
        config.get_active_project.return_value = proj
        register_build_tools(mcp, lambda: config, MagicMock)
        tools = {t.name: t.fn for t in mcp._tool_manager.list_tools()}

        from unittest.mock import patch

        with patch(
            "unrealhub.tools.build_tools.UEPathResolver.resolve_from_uproject"
        ) as mock_resolve:
            mock_resolve.return_value = MagicMock()
            result = await tools["build_project"]("invalid_action")
        assert "unknown action" in result.lower()
