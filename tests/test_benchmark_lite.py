from unittest.mock import AsyncMock, patch

import pytest

from unrealhub.config import ProjectConfig
from unrealhub.state import StateStore


class TestBenchmarkLite:
    @pytest.mark.asyncio
    @patch("unrealhub.benchmark_lite._list_domains_and_counts", new_callable=AsyncMock)
    @patch("unrealhub.benchmark_lite._list_top_level_tools", new_callable=AsyncMock)
    @patch("unrealhub.benchmark_lite.run_benchmark_preflight", new_callable=AsyncMock)
    async def test_returns_preflight_only_when_blocked(
        self,
        mock_preflight,
        mock_tools,
        mock_domains,
        tmp_home,
    ):
        from unrealhub.benchmark_lite import run_benchmark_lite

        mock_preflight.return_value = {
            "agent": "codex",
            "model": "gpt-test",
            "project": "TestProject",
            "project_path": "configured (path masked)",
            "instance": "active instance",
            "endpoint": "reachable loopback endpoint",
            "checks": [],
            "allow_continue": False,
        }

        artifact = await run_benchmark_lite(
            config=ProjectConfig(),
            state=StateStore(),
        )

        assert artifact["artifact_type"] == "benchmark_lite"
        assert artifact["ready_for_next_level"] is False
        mock_tools.assert_not_awaited()
        mock_domains.assert_not_awaited()

    @pytest.mark.asyncio
    @patch("unrealhub.benchmark_lite._list_domains_and_counts", new_callable=AsyncMock)
    @patch("unrealhub.benchmark_lite._list_top_level_tools", new_callable=AsyncMock)
    @patch("unrealhub.benchmark_lite.run_benchmark_preflight", new_callable=AsyncMock)
    async def test_populates_inventory_when_preflight_passes(
        self,
        mock_preflight,
        mock_tools,
        mock_domains,
        tmp_home,
        fake_project,
        fake_engine,
    ):
        from unrealhub.benchmark_lite import run_benchmark_lite

        config = ProjectConfig()
        config.save_project("TestProject", str(fake_project), str(fake_engine), port=8422)
        mock_preflight.return_value = {
            "agent": "codex",
            "model": "gpt-test",
            "project": "TestProject",
            "project_path": "configured (path masked)",
            "instance": "active instance",
            "endpoint": "reachable loopback endpoint",
            "checks": [],
            "allow_continue": True,
        }
        mock_tools.return_value = ["get_dispatch", "get_unreal_state"]
        mock_domains.return_value = (["level", "slate"], {"level": 10, "slate": 22})

        artifact = await run_benchmark_lite(
            config=config,
            state=StateStore(),
            level="L0",
            scenario="smoke-connectivity-v1",
        )

        assert artifact["ready_for_next_level"] is True
        assert artifact["recommended_next_level"] == "L1"
        assert artifact["top_level_tools"] == ["get_dispatch", "get_unreal_state"]
        assert artifact["domain_tool_counts"]["slate"] == 22

    def test_format_report(self):
        from unrealhub.benchmark_lite import format_benchmark_lite_report

        artifact = {
            "benchmark_level": "L0",
            "scenario": "smoke-connectivity-v1",
            "project": "TestProject",
            "agent": "codex",
            "model": "gpt-test",
            "ready_for_next_level": True,
            "recommended_next_level": "L1",
            "top_level_tools": ["get_dispatch"],
            "domain_tool_counts": {"level": 10},
        }

        text = format_benchmark_lite_report(artifact)
        assert "Benchmark Lite" in text
        assert "Recommended next level: L1" in text

    def test_make_artifact_path(self, tmp_path):
        from unrealhub.benchmark_lite import make_benchmark_lite_artifact_path

        path = make_benchmark_lite_artifact_path(
            root_dir=str(tmp_path),
            level="L1",
            scenario="sandbox-prototype-v1",
        )

        assert path.parent.name == "artifacts"
        assert path.name.startswith("l1-sandbox-prototype-v1-lite-")
        assert path.suffix == ".json"

    def test_save_artifact(self, tmp_path):
        from unrealhub.benchmark_lite import save_benchmark_lite_artifact

        artifact = {
            "artifact_type": "benchmark_lite",
            "project_path": "configured (path masked)",
            "instance": "active instance",
        }
        output = tmp_path / "artifacts" / "lite.json"

        path = save_benchmark_lite_artifact(artifact, str(output))

        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "configured (path masked)" in text
