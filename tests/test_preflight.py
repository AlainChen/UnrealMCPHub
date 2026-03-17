from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from unrealhub.config import ProjectConfig
from unrealhub.state import StateStore


class TestBenchmarkPreflight:
    @pytest.mark.asyncio
    @patch("unrealhub.preflight.probe_unreal_mcp", new_callable=AsyncMock)
    async def test_returns_early_when_unconfigured(self, mock_probe, tmp_home):
        from unrealhub.preflight import run_benchmark_preflight

        report = await run_benchmark_preflight(
            config=ProjectConfig(),
            state=StateStore(),
        )

        assert report["allow_continue"] is False
        assert report["project"] == "unconfigured"
        mock_probe.assert_not_awaited()

    @pytest.mark.asyncio
    @patch("unrealhub.preflight.UEMCPClient")
    @patch("unrealhub.preflight.probe_unreal_mcp", new_callable=AsyncMock)
    async def test_all_checks_pass(self, mock_probe, mock_client_cls, tmp_home, fake_project, fake_engine):
        from unrealhub.preflight import run_benchmark_preflight

        config = ProjectConfig()
        config.save_project("TestProject", str(fake_project), str(fake_engine), port=8422)
        state = StateStore()
        state.upsert(port=8422, project_path=str(fake_project), url="http://127.0.0.1:8422/mcp", status="online")

        mock_probe.return_value = {"server_name": "Remote Unreal MCP"}
        metadata_client = MagicMock()
        metadata_client.call_tool = AsyncMock(return_value={"success": True, "content": [], "error": None})
        execution_client = MagicMock()
        execution_client.call_tool = AsyncMock(return_value={"success": True, "content": [], "error": None})
        mock_client_cls.side_effect = [metadata_client, execution_client]

        report = await run_benchmark_preflight(
            config=config,
            state=state,
            agent="codex",
            model="gpt-test",
        )

        assert report["allow_continue"] is True
        assert report["agent"] == "codex"
        assert report["model"] == "gpt-test"
        assert report["project_path"] == "configured (path masked)"
        assert report["endpoint"] == "reachable loopback endpoint"

    @pytest.mark.asyncio
    @patch("unrealhub.preflight.UEMCPClient")
    @patch("unrealhub.preflight.probe_unreal_mcp", new_callable=AsyncMock)
    async def test_execution_failure_blocks_continue(self, mock_probe, mock_client_cls, tmp_home, fake_project, fake_engine):
        from unrealhub.preflight import run_benchmark_preflight

        config = ProjectConfig()
        config.save_project("TestProject", str(fake_project), str(fake_engine), port=8422)
        state = StateStore()

        mock_probe.return_value = {"server_name": "Remote Unreal MCP"}
        metadata_client = MagicMock()
        metadata_client.call_tool = AsyncMock(return_value={"success": True, "content": [], "error": None})
        execution_client = MagicMock()
        execution_client.call_tool = AsyncMock(return_value={"success": False, "content": [], "error": "timeout"})
        mock_client_cls.side_effect = [metadata_client, execution_client]

        report = await run_benchmark_preflight(
            config=config,
            state=state,
        )

        assert report["allow_continue"] is False
        execution_check = next(c for c in report["checks"] if c["name"] == "execution_query")
        assert execution_check["detail"] == "timeout"


class TestBenchmarkArtifact:
    def test_build_artifact(self):
        from unrealhub.preflight import build_benchmark_artifact

        report = {
            "agent": "codex",
            "model": "gpt-test",
            "project": "TestProject",
            "project_path": "configured (path masked)",
            "instance": "unknown:8422",
            "endpoint": "reachable loopback endpoint",
            "checks": [{"name": "mcp_reachable", "ok": True, "detail": "reachable loopback endpoint"}],
            "allow_continue": False,
        }

        artifact = build_benchmark_artifact(report, level="L1", scenario="sandbox-prototype-v1")
        assert artifact["artifact_type"] == "benchmark_preflight"
        assert artifact["benchmark_level"] == "L1"
        assert artifact["scenario"] == "sandbox-prototype-v1"
        assert artifact["project_path"] == "configured (path masked)"
        assert artifact["instance"] == "active instance (project unresolved)"

    def test_save_artifact(self, tmp_path):
        from unrealhub.preflight import save_benchmark_artifact

        artifact = {
            "artifact_type": "benchmark_preflight",
            "project_path": "configured (path masked)",
            "endpoint": "reachable loopback endpoint",
        }
        output = tmp_path / "artifacts" / "preflight.json"

        path = save_benchmark_artifact(artifact, str(output))

        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "configured (path masked)" in text
        assert "reachable loopback endpoint" in text

    def test_make_default_artifact_path(self, tmp_path):
        from unrealhub.preflight import make_default_artifact_path

        path = make_default_artifact_path(
            root_dir=str(tmp_path),
            scenario="smoke-connectivity-v1",
            level="L0",
        )

        assert path.parent.name == "artifacts"
        assert path.name.startswith("l0-smoke-connectivity-v1-")
        assert path.suffix == ".json"
