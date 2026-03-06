import json
from pathlib import Path
from unittest.mock import patch

import pytest

from unrealhub.config import ProjectConfig, HubConfig, ProjectEntry, DEFAULT_PLUGIN_REPO


class TestHubConfig:
    def test_defaults(self):
        cfg = HubConfig()
        assert cfg.projects == {}
        assert cfg.active_project == ""
        assert cfg.scan_ports == [8422, 8423, 8424, 8425]
        assert cfg.plugin_repo == DEFAULT_PLUGIN_REPO
        assert cfg.plugin_local_cache == ""

    def test_project_entry(self):
        entry = ProjectEntry(
            uproject_path="/tmp/Test.uproject",
            engine_root="/tmp/UE",
            engine_association="5.5",
            mcp_port=8422,
        )
        assert entry.uproject_path == "/tmp/Test.uproject"
        assert entry.mcp_port == 8422
        assert entry.configured_at == ""


class TestProjectConfig:
    def test_empty_config(self, tmp_home):
        cfg = ProjectConfig()
        assert not cfg.is_configured()
        assert cfg.get_active_project() is None
        assert cfg.get_active_project_name() == ""
        assert cfg.list_projects() == {}

    def test_save_and_load_project(self, tmp_home):
        cfg = ProjectConfig()
        entry = cfg.save_project("MyProject", "/tmp/My.uproject", "/tmp/UE", "5.5", 8422)
        assert entry.uproject_path == "/tmp/My.uproject"
        assert cfg.is_configured()
        assert cfg.get_active_project_name() == "MyProject"
        assert cfg.get_active_project().uproject_path == "/tmp/My.uproject"

        cfg2 = ProjectConfig()
        assert cfg2.is_configured()
        assert cfg2.get_active_project_name() == "MyProject"

    def test_multiple_projects(self, tmp_home):
        cfg = ProjectConfig()
        cfg.save_project("A", "/a.uproject", "/e1")
        cfg.save_project("B", "/b.uproject", "/e2")
        projects = cfg.list_projects()
        assert len(projects) == 2
        assert "A" in projects
        assert "B" in projects
        assert cfg.get_active_project_name() == "A"

    def test_set_active_project(self, tmp_home):
        cfg = ProjectConfig()
        cfg.save_project("A", "/a.uproject", "/e1")
        cfg.save_project("B", "/b.uproject", "/e2")
        assert cfg.set_active_project("B")
        assert cfg.get_active_project_name() == "B"
        assert not cfg.set_active_project("NonExistent")

    def test_remove_project(self, tmp_home):
        cfg = ProjectConfig()
        cfg.save_project("A", "/a.uproject", "/e1")
        cfg.save_project("B", "/b.uproject", "/e2")
        cfg.set_active_project("A")

        assert cfg.remove_project("A")
        assert cfg.get_active_project_name() == "B"
        assert len(cfg.list_projects()) == 1

    def test_remove_nonexistent(self, tmp_home):
        cfg = ProjectConfig()
        assert not cfg.remove_project("ghost")

    def test_remove_last_project(self, tmp_home):
        cfg = ProjectConfig()
        cfg.save_project("Only", "/only.uproject", "/e")
        assert cfg.remove_project("Only")
        assert cfg.get_active_project_name() == ""
        assert not cfg.is_configured()

    def test_scan_ports(self, tmp_home):
        cfg = ProjectConfig()
        ports = cfg.get_scan_ports()
        assert ports == [8422, 8423, 8424, 8425]
        assert ports is not cfg._config.scan_ports

    def test_plugin_repo(self, tmp_home):
        cfg = ProjectConfig()
        assert cfg.get_plugin_repo() == DEFAULT_PLUGIN_REPO
        cfg.set_plugin_repo("https://example.com/repo.zip")
        assert cfg.get_plugin_repo() == "https://example.com/repo.zip"

        cfg2 = ProjectConfig()
        assert cfg2.get_plugin_repo() == "https://example.com/repo.zip"

    def test_plugin_cache(self, tmp_home):
        cfg = ProjectConfig()
        assert cfg.get_plugin_cache() == ""
        cfg.set_plugin_cache("/tmp/cache")
        assert cfg.get_plugin_cache() == "/tmp/cache"

    def test_load_corrupted_json(self, tmp_home):
        (tmp_home / "config.json").write_text("NOT JSON", encoding="utf-8")
        cfg = ProjectConfig()
        assert not cfg.is_configured()

    def test_first_project_auto_activates(self, tmp_home):
        cfg = ProjectConfig()
        cfg.save_project("First", "/first.uproject", "/e")
        assert cfg.get_active_project_name() == "First"

    def test_second_project_does_not_override_active(self, tmp_home):
        cfg = ProjectConfig()
        cfg.save_project("First", "/first.uproject", "/e")
        cfg.save_project("Second", "/second.uproject", "/e")
        assert cfg.get_active_project_name() == "First"
