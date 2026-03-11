import json
from pathlib import Path
from unittest.mock import patch

import pytest

from unrealhub.state import StateStore, InstanceState, Note, ToolCallRecord, make_key


class TestMakeKey:
    def test_with_project(self):
        assert make_key("G:/Proj/Develop57.uproject", 8422) == "Develop57:8422"

    def test_without_project(self):
        assert make_key("", 8422) == "unknown:8422"

    def test_path_stem(self):
        assert make_key("C:/Users/me/MyGame/MyGame.uproject", 9000) == "MyGame:9000"


class TestStateStore:
    def test_empty_state(self, tmp_home):
        store = StateStore()
        assert store.list_instances() == []
        assert store.get_active_instance() is None

    def test_upsert_creates_instance(self, tmp_home):
        store = StateStore()
        inst = store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=1234)
        assert inst.key == "A:8422"
        assert inst.port == 8422
        assert inst.pid == 1234
        assert inst.status == "online"
        assert store.get_active_instance().key == "A:8422"

    def test_upsert_updates_existing(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=1000)
        inst = store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=2000)
        assert inst.pid == 2000
        assert len(store.list_instances()) == 1

    def test_upsert_different_ports(self, tmp_home):
        store = StateStore()
        i1 = store.upsert(port=8422, project_path="G:/Proj/A.uproject")
        i2 = store.upsert(port=8423, project_path="G:/Proj/B.uproject")
        assert i1.key == "A:8422"
        assert i2.key == "B:8423"
        assert len(store.list_instances()) == 2

    def test_upsert_port_conflict_marks_old_offline(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", status="online")
        store.upsert(port=8422, project_path="G:/Proj/B.uproject", status="online")
        a = store.get_instance("A:8422")
        b = store.get_instance("B:8422")
        assert a.status == "offline"
        assert b.status == "online"

    def test_upsert_unknown_upgrade(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422)
        assert store.get_instance("unknown:8422") is not None
        inst = store.upsert(port=8422, project_path="G:/Proj/A.uproject")
        assert inst.key == "A:8422"
        assert store.get_instance("unknown:8422") is None
        assert len(store.list_instances()) == 1

    def test_upsert_without_pid_is_offline(self, tmp_home):
        store = StateStore()
        inst = store.upsert(port=8422, status="offline")
        assert inst.status == "offline"

    def test_unregister_instance(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject")
        assert store.unregister_instance("A:8422")
        assert store.list_instances() == []
        assert store.get_active_instance() is None

    def test_unregister_active_fallback(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject")
        store.upsert(port=8423, project_path="G:/Proj/B.uproject")
        store.set_active("A:8422")
        store.unregister_instance("A:8422")
        active = store.get_active_instance()
        assert active is not None
        assert active.key == "B:8423"

    def test_unregister_nonexistent(self, tmp_home):
        store = StateStore()
        assert not store.unregister_instance("ghost")

    def test_get_instance_by_key(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject")
        inst = store.get_instance("A:8422")
        assert inst is not None
        assert inst.port == 8422
        assert store.get_instance("ghost:9999") is None

    def test_get_instance_by_port(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject")
        inst = store.get_instance("8422")
        assert inst is not None
        assert inst.key == "A:8422"

    def test_get_instance_by_project_name(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/MyGame.uproject")
        inst = store.get_instance("MyGame")
        assert inst is not None
        assert inst.key == "MyGame:8422"

    def test_set_active(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject")
        store.upsert(port=8423, project_path="G:/Proj/B.uproject")
        assert store.set_active("B:8423")
        assert store.get_active_instance().key == "B:8423"
        assert not store.set_active("ghost")

    def test_update_status(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=5678)
        store.update_status("A:8422", "offline", pid=9999)
        inst = store.get_instance("A:8422")
        assert inst.status == "offline"
        assert inst.pid == 9999

    def test_update_status_nonexistent(self, tmp_home):
        store = StateStore()
        store.update_status("ghost", "online")

    def test_increment_crash_count(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject")
        store.increment_crash_count("A:8422")
        inst = store.get_instance("A:8422")
        assert inst.crash_count == 1
        assert inst.status == "offline"
        store.increment_crash_count("A:8422")
        inst = store.get_instance("A:8422")
        assert inst.crash_count == 2

    def test_add_and_get_notes(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject")
        store.add_note("A:8422", "Test note")
        store.add_note("A:8422", "Another note")
        notes = store.get_notes("A:8422")
        assert len(notes) == 2
        assert notes[0].content == "Test note"
        assert notes[1].content == "Another note"

    def test_get_notes_nonexistent(self, tmp_home):
        store = StateStore()
        assert store.get_notes("ghost") == []

    def test_record_tool_call(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject")
        store.record_tool_call("A:8422", "test_tool", True, 42.5)
        store.record_tool_call("A:8422", "other_tool", False, 100.0)
        history = store.get_call_history("A:8422")
        assert len(history) == 2
        assert history[0].tool_name == "test_tool"
        assert history[0].success is True
        assert history[0].duration_ms == 42.5

    def test_get_call_history_with_limit(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject")
        for i in range(10):
            store.record_tool_call("A:8422", f"tool_{i}", True, 1.0)
        history = store.get_call_history("A:8422", limit=3)
        assert len(history) == 3
        assert history[0].tool_name == "tool_7"

    def test_get_call_history_nonexistent(self, tmp_home):
        store = StateStore()
        assert store.get_call_history("ghost") == []

    def test_list_instances_summary(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/Dev.uproject")
        summary = store.list_instances_summary()
        assert "Dev:8422" in summary
        assert "*" in summary

    def test_list_instances_summary_empty(self, tmp_home):
        store = StateStore()
        assert "(no instances)" in store.list_instances_summary()

    def test_persist_and_reload(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=999)
        store.add_note("A:8422", "persisted note")
        store.save()

        store2 = StateStore()
        inst = store2.get_instance("A:8422")
        assert inst is not None
        assert inst.pid == 999
        notes = store2.get_notes("A:8422")
        assert len(notes) == 1

    def test_load_corrupted_state(self, tmp_home):
        (tmp_home / "state.json").write_text("BROKEN", encoding="utf-8")
        store = StateStore()
        assert store.list_instances() == []

    def test_resolve_by_port(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/Game.uproject")
        assert store.set_active("8422")
        assert store.get_active_instance().key == "Game:8422"

    def test_cleanup(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", status="offline")
        store._instances["A:8422"].last_seen = "2020-01-01T00:00:00"
        removed = store.cleanup(max_age_hours=0.001)
        assert "A:8422" in removed
        assert len(store.list_instances()) == 0

    def test_cleanup_keeps_online(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", status="online")
        store._instances["A:8422"].last_seen = "2020-01-01T00:00:00"
        removed = store.cleanup(max_age_hours=0.001)
        assert removed == []
        assert len(store.list_instances()) == 1

    def test_find_by_project_path(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject")
        store.upsert(port=8423, project_path="G:/Proj/B.uproject")
        found = store.find_by_project_path("G:/Proj/A.uproject")
        assert len(found) == 1
        assert found[0].key == "A:8422"

    def test_find_by_port(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject")
        found = store.find_by_port(8422)
        assert len(found) == 1
        assert found[0].key == "A:8422"


class TestPort0OrphanProcess:
    """Tests for port=0 (no MCP) instances and upgrade to real ports."""

    def test_upsert_port0_creates_instance(self, tmp_home):
        store = StateStore()
        inst = store.upsert(port=0, project_path="G:/Proj/A.uproject", pid=1234, status="offline")
        assert inst.key == "A:0"
        assert inst.port == 0
        assert inst.status == "offline"
        assert inst.url == ""

    def test_port0_upgrade_to_real_port(self, tmp_home):
        store = StateStore()
        store.upsert(port=0, project_path="G:/Proj/A.uproject", pid=1234, status="offline")
        assert store.get_instance("A:0") is not None
        inst = store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=1234, status="online")
        assert inst.key == "A:8422"
        assert inst.status == "online"
        assert inst.port == 8422
        assert store.get_instance("A:0") is None
        assert len(store.list_instances()) == 1

    def test_port0_upgrade_preserves_notes(self, tmp_home):
        store = StateStore()
        store.upsert(port=0, project_path="G:/Proj/A.uproject", pid=1234, status="offline")
        store.add_note("A:0", "from orphan phase")
        inst = store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=1234, status="online")
        assert inst.key == "A:8422"
        notes = store.get_notes("A:8422")
        assert len(notes) == 1
        assert notes[0].content == "from orphan phase"

    def test_port0_upgrade_active_reassigned(self, tmp_home):
        store = StateStore()
        store.upsert(port=0, project_path="G:/Proj/A.uproject", pid=1234, status="offline")
        store.set_active("A:0")
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=1234, status="online")
        active = store.get_active_instance()
        assert active is not None
        assert active.key == "A:8422"

    def test_summary_shows_no_mcp_tag(self, tmp_home):
        store = StateStore()
        store.upsert(port=0, project_path="G:/Proj/A.uproject", pid=1234, status="offline")
        summary = store.list_instances_summary()
        assert "[NO MCP]" in summary
        assert "A:0" in summary

    def test_summary_no_tag_for_real_port(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=1234)
        summary = store.list_instances_summary()
        assert "[NO MCP]" not in summary


class TestV1Migration:
    def test_migrate_v1_to_v2(self, tmp_home):
        v1_data = {
            "instances": {
                "ue1": {
                    "auto_id": "ue1", "url": "http://localhost:8422/mcp",
                    "port": 8422, "project_path": "G:/Proj/A.uproject",
                    "status": "online", "first_seen": "2026-01-01",
                    "last_seen": "2026-01-02", "last_health_check": "2026-01-02",
                    "crash_count": 0, "alias": "dev",
                    "metrics": {"cpu_percent": 0, "memory_mb": 0, "last_updated": ""},
                },
                "ue2": {
                    "auto_id": "ue2", "url": "http://localhost:8422/mcp",
                    "port": 8422, "project_path": "G:/Proj/A.uproject",
                    "status": "crashed", "first_seen": "2026-01-01",
                    "last_seen": "2026-01-01", "last_health_check": "",
                    "crash_count": 1,
                    "metrics": {"cpu_percent": 0, "memory_mb": 0, "last_updated": ""},
                },
            },
            "active_instance_id": "ue1",
            "next_id": 3,
        }
        (tmp_home / "state.json").write_text(json.dumps(v1_data), encoding="utf-8")

        store = StateStore()
        instances = store.list_instances()
        assert len(instances) == 1
        inst = instances[0]
        assert inst.key == "A:8422"
        assert inst.last_seen == "2026-01-02"
        assert inst.status == "online"
        active = store.get_active_instance()
        assert active is not None
        assert active.key == "A:8422"
