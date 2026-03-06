import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
import psutil

from unrealhub.utils.process import (
    find_project_from_cmdline,
    is_process_alive,
    get_process_info,
    find_crash_dirs,
    find_unreal_editor_processes,
)


class TestFindProjectFromCmdline:
    def test_with_uproject(self):
        cmdline = [
            "D:\\UE\\Editor.exe",
            "C:\\Projects\\MyGame.uproject",
            "-log",
        ]
        assert find_project_from_cmdline(cmdline) == "C:\\Projects\\MyGame.uproject"

    def test_with_spaces(self):
        cmdline = ["editor.exe", "  /path/to/My Game.uproject  "]
        result = find_project_from_cmdline(cmdline)
        assert result == "/path/to/My Game.uproject"

    def test_no_uproject(self):
        cmdline = ["editor.exe", "-game", "-log"]
        assert find_project_from_cmdline(cmdline) is None

    def test_empty_cmdline(self):
        assert find_project_from_cmdline([]) is None
        assert find_project_from_cmdline(None) is None

    def test_case_insensitive(self):
        cmdline = ["editor.exe", "Test.UPROJECT"]
        assert find_project_from_cmdline(cmdline) == "Test.UPROJECT"


class TestIsProcessAlive:
    def test_current_process(self):
        assert is_process_alive(os.getpid())

    def test_nonexistent_pid(self):
        assert not is_process_alive(999999999)


class TestGetProcessInfo:
    def test_current_process(self):
        info = get_process_info(os.getpid())
        assert info is not None
        assert info["pid"] == os.getpid()
        assert "memory_mb" in info
        assert "status" in info

    def test_nonexistent_process(self):
        info = get_process_info(999999999)
        assert info is None


class TestFindCrashDirs:
    def test_no_crashes_dir(self, tmp_path):
        result = find_crash_dirs(str(tmp_path))
        assert result == []

    def test_empty_crashes_dir(self, tmp_path):
        crashes = tmp_path / "Saved" / "Crashes"
        crashes.mkdir(parents=True)
        result = find_crash_dirs(str(tmp_path))
        assert result == []

    def test_with_crash_dirs(self, tmp_path):
        crashes = tmp_path / "Saved" / "Crashes"
        crash1 = crashes / "CRASH-001"
        crash2 = crashes / "CRASH-002"
        crash1.mkdir(parents=True)
        crash2.mkdir(parents=True)
        (crash1 / "dummy.txt").write_text("x")

        result = find_crash_dirs(str(tmp_path))
        assert len(result) == 2
        names = [r["name"] for r in result]
        assert "CRASH-001" in names
        assert "CRASH-002" in names

    def test_sorted_by_mtime(self, tmp_path):
        import time
        crashes = tmp_path / "Saved" / "Crashes"
        old = crashes / "OLD"
        old.mkdir(parents=True)
        (old / "x.txt").write_text("x")
        time.sleep(0.05)
        new = crashes / "NEW"
        new.mkdir(parents=True)
        (new / "x.txt").write_text("x")

        result = find_crash_dirs(str(tmp_path))
        assert result[0]["name"] == "NEW"


class TestFindUnrealEditorProcesses:
    def test_with_mock(self):
        mock_proc = MagicMock()
        mock_proc.info = {
            "pid": 1234,
            "name": "UnrealEditor.exe",
            "cmdline": ["UnrealEditor.exe", "C:/Test.uproject"],
        }
        with patch("psutil.process_iter", return_value=[mock_proc]):
            procs = find_unreal_editor_processes()
            assert len(procs) == 1
            assert procs[0]["pid"] == 1234
            assert procs[0]["project_path"] == "C:/Test.uproject"

    def test_filters_non_ue(self):
        mock_proc = MagicMock()
        mock_proc.info = {"pid": 1, "name": "chrome.exe", "cmdline": []}
        with patch("psutil.process_iter", return_value=[mock_proc]):
            procs = find_unreal_editor_processes()
            assert procs == []

    def test_handles_access_denied(self):
        mock_proc = MagicMock()
        mock_proc.info.__getitem__ = MagicMock(
            side_effect=psutil.AccessDenied(1)
        )
        type(mock_proc).info = property(
            lambda self: (_ for _ in ()).throw(psutil.AccessDenied(1))
        )
        with patch("psutil.process_iter", return_value=[mock_proc]):
            procs = find_unreal_editor_processes()
            assert procs == []
