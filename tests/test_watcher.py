import asyncio
import time
from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from unrealhub.watcher import ProcessWatcher
from unrealhub.state import StateStore, InstanceState


class TestProcessWatcher:
    def _make_state(self, tmp_home):
        store = StateStore()
        return store

    def test_start_stop(self, tmp_home):
        store = self._make_state(tmp_home)
        watcher = ProcessWatcher(lambda: store, interval=0.1)
        watcher.start()
        assert watcher._thread is not None
        assert watcher._thread.is_alive()

        watcher.start()

        watcher.stop()
        assert not watcher._thread.is_alive()

    def test_on_crash_callback(self, tmp_home):
        store = self._make_state(tmp_home)
        watcher = ProcessWatcher(lambda: store, interval=60)
        crashed_ids = []
        watcher.on_crash(lambda iid: crashed_ids.append(iid))
        assert len(watcher._on_crash_callbacks) == 1

    @pytest.mark.asyncio
    async def test_check_all_skips_offline(self, tmp_home):
        store = self._make_state(tmp_home)
        store.register_instance(url="http://localhost:8422/mcp", port=8422)
        store.update_status("ue1", "offline")

        watcher = ProcessWatcher(lambda: store, interval=60)
        with patch.object(watcher, "_check_instance", new_callable=AsyncMock) as mock_check:
            await watcher._check_all()
            mock_check.assert_not_called()

    @pytest.mark.asyncio
    async def test_check_all_checks_online(self, tmp_home):
        store = self._make_state(tmp_home)
        store.register_instance(url="http://localhost:8422/mcp", port=8422, pid=1234)

        watcher = ProcessWatcher(lambda: store, interval=60)
        with patch.object(watcher, "_check_instance", new_callable=AsyncMock) as mock_check:
            await watcher._check_all()
            mock_check.assert_called_once()

    @pytest.mark.asyncio
    async def test_check_instance_crash(self, tmp_home):
        store = self._make_state(tmp_home)
        inst = store.register_instance(
            url="http://localhost:8422/mcp", port=8422, pid=99999
        )
        store.update_status("ue1", "online")

        crashed_ids = []
        watcher = ProcessWatcher(lambda: store, interval=60)
        watcher.on_crash(lambda iid: crashed_ids.append(iid))

        with patch("unrealhub.utils.process.is_process_alive", return_value=False), \
             patch("unrealhub.ue_client.UEMCPClient.probe_endpoint", new_callable=AsyncMock, return_value=False):
            await watcher._check_instance(store, store.get_instance("ue1"))

        updated = store.get_instance("ue1")
        assert updated.status == "crashed"
        assert updated.crash_count == 1
        assert "ue1" in crashed_ids

    @pytest.mark.asyncio
    async def test_check_instance_healthy(self, tmp_home):
        store = self._make_state(tmp_home)
        store.register_instance(url="http://localhost:8422/mcp", port=8422, pid=1234)

        watcher = ProcessWatcher(lambda: store, interval=60)

        with patch("unrealhub.utils.process.is_process_alive", return_value=True), \
             patch("unrealhub.ue_client.UEMCPClient.probe_endpoint", new_callable=AsyncMock, return_value=True):
            await watcher._check_instance(store, store.get_instance("ue1"))

        updated = store.get_instance("ue1")
        assert updated.status == "online"

    @pytest.mark.asyncio
    async def test_check_instance_pid_alive_http_down(self, tmp_home):
        store = self._make_state(tmp_home)
        store.register_instance(url="http://localhost:8422/mcp", port=8422, pid=1234)

        watcher = ProcessWatcher(lambda: store, interval=60)

        with patch("unrealhub.utils.process.is_process_alive", return_value=True), \
             patch("unrealhub.ue_client.UEMCPClient.probe_endpoint", new_callable=AsyncMock, return_value=False):
            await watcher._check_instance(store, store.get_instance("ue1"))

        updated = store.get_instance("ue1")
        assert updated.status == "offline"

    @pytest.mark.asyncio
    async def test_no_double_crash(self, tmp_home):
        store = self._make_state(tmp_home)
        store.register_instance(url="http://localhost:8422/mcp", port=8422, pid=99999)
        store.update_status("ue1", "crashed")
        store.increment_crash_count("ue1")

        watcher = ProcessWatcher(lambda: store, interval=60)
        with patch("unrealhub.utils.process.is_process_alive", return_value=False), \
             patch("unrealhub.ue_client.UEMCPClient.probe_endpoint", new_callable=AsyncMock, return_value=False):
            await watcher._check_instance(store, store.get_instance("ue1"))

        assert store.get_instance("ue1").crash_count == 1
