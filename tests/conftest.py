import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.fixture()
def tmp_home(tmp_path):
    """Redirect ~/.unrealhub to a temp directory."""
    hub_dir = tmp_path / ".unrealhub"
    hub_dir.mkdir()
    with patch("unrealhub.config.CONFIG_DIR", hub_dir), \
         patch("unrealhub.config.CONFIG_PATH", hub_dir / "config.json"), \
         patch("unrealhub.state.STATE_PATH", hub_dir / "state.json"):
        yield hub_dir


@pytest.fixture()
def fake_project(tmp_path):
    """Create a minimal .uproject file and return its path."""
    proj_dir = tmp_path / "TestProject"
    proj_dir.mkdir()
    uproject = proj_dir / "TestProject.uproject"
    uproject.write_text(json.dumps({
        "FileVersion": 3,
        "EngineAssociation": "5.5",
        "Plugins": [],
    }), encoding="utf-8")
    return uproject


@pytest.fixture()
def fake_engine(tmp_path):
    """Create a fake engine directory with expected binaries."""
    engine = tmp_path / "FakeEngine"
    bins = [
        "Engine/Binaries/DotNET/UnrealBuildTool/UnrealBuildTool.exe",
        "Engine/Build/BatchFiles/RunUAT.bat",
        "Engine/Binaries/Win64/UnrealEditor.exe",
        "Engine/Build/BatchFiles/Build.bat",
    ]
    for rel in bins:
        p = engine / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("dummy", encoding="utf-8")
    return engine
