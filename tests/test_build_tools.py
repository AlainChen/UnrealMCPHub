import pytest

from unrealhub.tools.build_tools import _analyze_build_output


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
