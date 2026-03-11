"""Tests for cleanup (stale instance removal) and offline marking logic."""
from unittest.mock import patch
from datetime import datetime, timedelta

import pytest

from unrealhub.state import StateStore


class TestCleanup:
    """StateStore.cleanup(): remove stale offline instances."""

    def test_noop_when_all_online(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=100, status="online")
        store._instances["A:8422"].last_seen = "2020-01-01T00:00:00"
        removed = store.cleanup(max_age_hours=0.001)
        assert removed == []
        assert len(store.list_instances()) == 1

    def test_removes_stale_offline(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", status="offline")
        store._instances["A:8422"].last_seen = "2020-01-01T00:00:00"
        removed = store.cleanup(max_age_hours=0.001)
        assert "A:8422" in removed
        assert len(store.list_instances()) == 0

    def test_keeps_recent_offline(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", status="offline")
        removed = store.cleanup(max_age_hours=24.0)
        assert removed == []
        assert len(store.list_instances()) == 1

    def test_removes_multiple_stale(self, tmp_home):
        store = StateStore()
        for port in (8422, 8423, 8424):
            store.upsert(port=port, project_path=f"G:/Proj/{chr(65+port-8422)}.uproject", status="offline")
            key = f"{chr(65+port-8422)}:{port}"
            store._instances[key].last_seen = "2020-01-01T00:00:00"
        removed = store.cleanup(max_age_hours=0.001)
        assert len(removed) == 3
        assert len(store.list_instances()) == 0

    def test_mixed_online_and_stale(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=100, status="online")
        store.upsert(port=8423, project_path="G:/Proj/B.uproject", status="offline")
        store._instances["B:8423"].last_seen = "2020-01-01T00:00:00"
        removed = store.cleanup(max_age_hours=0.001)
        assert "B:8423" in removed
        assert len(store.list_instances()) == 1
        assert store.list_instances()[0].key == "A:8422"

    def test_active_reassigned_on_removal(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=100, status="online")
        store.upsert(port=8423, project_path="G:/Proj/B.uproject", status="offline")
        store.set_active("B:8423")
        store._instances["B:8423"].last_seen = "2020-01-01T00:00:00"
        store.cleanup(max_age_hours=0.001)
        active = store.get_active_instance()
        assert active is not None
        assert active.key == "A:8422"


class TestOfflineMarking:
    """Instances go offline when port stops responding and PID is dead."""

    def test_update_status_to_offline(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=100, status="online")
        store.update_status("A:8422", "offline")
        assert store.get_instance("A:8422").status == "offline"

    def test_increment_crash_count(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=100, status="online")
        store.increment_crash_count("A:8422")
        inst = store.get_instance("A:8422")
        assert inst.crash_count == 1
        assert inst.status == "offline"

    def test_upsert_back_to_online(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", status="offline")
        inst = store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=200, status="online")
        assert inst.status == "online"

    def test_port_conflict_marks_old_offline(self, tmp_home):
        store = StateStore()
        store.upsert(port=8422, project_path="G:/Proj/A.uproject", pid=100, status="online")
        store.upsert(port=8422, project_path="G:/Proj/B.uproject", pid=200, status="online")
        assert store.get_instance("A:8422").status == "offline"
        assert store.get_instance("B:8422").status == "online"
