import json
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from unrealhub.tools.install_tools import (
    _copy_and_enable,
    _enable_plugins_in_uproject,
    _find_local_plugin,
)


class TestEnablePluginsInUproject:
    def test_enables_missing_plugins(self, tmp_path):
        uproject = tmp_path / "Test.uproject"
        uproject.write_text(json.dumps({
            "FileVersion": 3,
            "Plugins": [],
        }), encoding="utf-8")

        result = _enable_plugins_in_uproject(str(uproject))
        assert "enabled" in result.lower()

        data = json.loads(uproject.read_text(encoding="utf-8"))
        names = {p["Name"] for p in data["Plugins"]}
        assert "PythonScriptPlugin" in names
        assert "RemoteMCP" in names
        for p in data["Plugins"]:
            assert p["Enabled"] is True

    def test_enables_disabled_plugin(self, tmp_path):
        uproject = tmp_path / "Test.uproject"
        uproject.write_text(json.dumps({
            "FileVersion": 3,
            "Plugins": [
                {"Name": "RemoteMCP", "Enabled": False},
            ],
        }), encoding="utf-8")

        _enable_plugins_in_uproject(str(uproject))
        data = json.loads(uproject.read_text(encoding="utf-8"))
        remote = [p for p in data["Plugins"] if p["Name"] == "RemoteMCP"][0]
        assert remote["Enabled"] is True

    def test_already_enabled(self, tmp_path):
        uproject = tmp_path / "Test.uproject"
        uproject.write_text(json.dumps({
            "FileVersion": 3,
            "Plugins": [
                {"Name": "PythonScriptPlugin", "Enabled": True},
                {"Name": "RemoteMCP", "Enabled": True},
            ],
        }), encoding="utf-8")

        result = _enable_plugins_in_uproject(str(uproject))
        assert "already" in result.lower()

    def test_no_plugins_key(self, tmp_path):
        uproject = tmp_path / "Test.uproject"
        uproject.write_text(json.dumps({"FileVersion": 3}), encoding="utf-8")

        _enable_plugins_in_uproject(str(uproject))
        data = json.loads(uproject.read_text(encoding="utf-8"))
        assert "Plugins" in data
        assert len(data["Plugins"]) == 2

    def test_invalid_file(self, tmp_path):
        uproject = tmp_path / "Bad.uproject"
        uproject.write_text("NOT JSON", encoding="utf-8")
        result = _enable_plugins_in_uproject(str(uproject))
        assert "failed" in result.lower()


class TestCopyAndEnable:
    def _make_plugin_source(self, tmp_path):
        source = tmp_path / "source_plugin"
        source.mkdir()
        (source / "RemoteMCP.uplugin").write_text("{}", encoding="utf-8")
        (source / "Source").mkdir()
        (source / "Source" / "test.cpp").write_text("//", encoding="utf-8")
        (source / "__pycache__").mkdir()
        (source / "__pycache__" / "junk.pyc").write_bytes(b"x")
        return source

    def test_copy_success(self, tmp_path):
        source = self._make_plugin_source(tmp_path)
        uproject = tmp_path / "Test.uproject"
        uproject.write_text(json.dumps({"FileVersion": 3, "Plugins": []}),
                            encoding="utf-8")
        dest = tmp_path / "Plugins" / "RemoteMCP"

        result = _copy_and_enable(source, dest, uproject)
        assert "installed" in result.lower()
        assert dest.exists()
        assert (dest / "RemoteMCP.uplugin").exists()
        assert not (dest / "__pycache__").exists()

    def test_copy_failure(self, tmp_path):
        source = tmp_path / "nonexistent"
        uproject = tmp_path / "Test.uproject"
        uproject.write_text("{}", encoding="utf-8")
        dest = tmp_path / "Plugins" / "RemoteMCP"

        result = _copy_and_enable(source, dest, uproject)
        assert "failed" in result.lower()


class TestFindLocalPlugin:
    def test_finds_cache(self, tmp_path):
        cache_dir = tmp_path / "cached_plugin"
        cache_dir.mkdir()
        (cache_dir / "RemoteMCP.uplugin").write_text("{}", encoding="utf-8")

        config = MagicMock()
        config.get_plugin_cache.return_value = str(cache_dir)

        result = _find_local_plugin(config, tmp_path / "project")
        assert result == str(cache_dir)

    def test_no_cache_no_sibling_no_project(self, tmp_path):
        config = MagicMock()
        config.get_plugin_cache.return_value = ""
        project_dir = tmp_path / "empty_project"
        project_dir.mkdir()
        result = _find_local_plugin(config, project_dir)
        # May find sibling RemoteMCP from workspace or return None
        if result is not None:
            assert Path(result).is_dir()

    def test_finds_in_project_plugins(self, tmp_path):
        project_dir = tmp_path / "project"
        plugin_dir = project_dir / "Plugins" / "RemoteMCP"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "RemoteMCP.uplugin").write_text("{}", encoding="utf-8")

        config = MagicMock()
        config.get_plugin_cache.return_value = ""

        result = _find_local_plugin(config, project_dir)
        assert result is not None
        assert "RemoteMCP" in result
