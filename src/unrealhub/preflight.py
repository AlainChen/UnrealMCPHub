from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from unrealhub.config import ProjectConfig, ProjectEntry
from unrealhub.state import InstanceState, StateStore
from unrealhub.tools.discovery_tools import probe_unreal_mcp
from unrealhub.ue_client import UEMCPClient


@dataclass
class PreflightCheck:
    name: str
    ok: bool
    detail: str


def _masked_path_label(path: str) -> str:
    if not path:
        return "not configured"
    return "configured (path masked)"


def _masked_url_label(url: str) -> str:
    if not url:
        return "not available"
    return "reachable loopback endpoint" if "127.0.0.1" in url or "localhost" in url else "reachable endpoint"


def _masked_instance_label(instance_key: str) -> str:
    if not instance_key:
        return "not identified"
    if instance_key.startswith("unknown:"):
        return "active instance (project unresolved)"
    return "active instance"


async def _resolve_instance_url(
    config: ProjectConfig,
    state: StateStore,
    instance_id: str | None,
) -> tuple[InstanceState | None, str]:
    inst = state.get_instance(instance_id) if instance_id else state.get_active_instance()
    if inst and inst.url:
        return inst, inst.url

    proj = config.get_active_project()
    if not proj:
        return None, ""

    return None, f"http://127.0.0.1:{proj.mcp_port}/mcp"


async def run_benchmark_preflight(
    *,
    config: ProjectConfig,
    state: StateStore,
    instance_id: str | None = None,
    metadata_timeout: float = 8.0,
    execution_timeout: float = 8.0,
    agent: str = "",
    model: str = "",
) -> dict[str, Any]:
    proj: ProjectEntry | None = config.get_active_project()
    checks: list[PreflightCheck] = []
    summary: dict[str, Any] = {
        "agent": agent or "unspecified",
        "model": model or "unspecified",
        "project": config.get_active_project_name() or "unconfigured",
        "project_path": _masked_path_label(proj.uproject_path if proj else ""),
        "instance": "not identified",
        "endpoint": "not available",
        "checks": [],
        "allow_continue": False,
    }

    checks.append(
        PreflightCheck(
            name="project_configured",
            ok=proj is not None,
            detail=_masked_path_label(proj.uproject_path if proj else ""),
        )
    )
    if proj is None:
        summary["checks"] = [c.__dict__ for c in checks]
        return summary

    inst, url = await _resolve_instance_url(config, state, instance_id)
    checks.append(
        PreflightCheck(
            name="active_instance_identified",
            ok=bool(inst or url),
            detail=_masked_instance_label(inst.key) if inst else "derived from configured project port",
        )
    )
    summary["instance"] = _masked_instance_label(inst.key) if inst else "derived from configured project port"
    summary["endpoint"] = _masked_url_label(url)

    if not url:
        summary["checks"] = [c.__dict__ for c in checks]
        return summary

    probe = await probe_unreal_mcp(url, timeout=3.0)
    checks.append(
        PreflightCheck(
            name="mcp_reachable",
            ok=probe is not None,
            detail=_masked_url_label(url) if probe else "probe failed",
        )
    )
    if probe is None:
        summary["checks"] = [c.__dict__ for c in checks]
        return summary

    client = UEMCPClient(url, timeout_connect=3.0, timeout_read=metadata_timeout)
    metadata = await client.call_tool("get_dispatch", {})
    checks.append(
        PreflightCheck(
            name="metadata_query",
            ok=metadata.get("success", False),
            detail="get_dispatch succeeded" if metadata.get("success") else (metadata.get("error") or "metadata query failed"),
        )
    )

    exec_client = UEMCPClient(url, timeout_connect=3.0, timeout_read=execution_timeout)
    execution = await exec_client.call_tool("get_unreal_state", {})
    checks.append(
        PreflightCheck(
            name="execution_query",
            ok=execution.get("success", False),
            detail="get_unreal_state succeeded" if execution.get("success") else (execution.get("error") or "execution query failed"),
        )
    )

    summary["checks"] = [c.__dict__ for c in checks]
    summary["allow_continue"] = all(c.ok for c in checks)
    return summary


def build_benchmark_artifact(
    report: dict[str, Any],
    *,
    level: str = "L0",
    scenario: str = "benchmark-preflight",
) -> dict[str, Any]:
    instance_label = report.get("instance", "")
    if instance_label.startswith("unknown:"):
        instance_label = _masked_instance_label(instance_label)

    return {
        "artifact_type": "benchmark_preflight",
        "generated_at": datetime.now().isoformat(),
        "benchmark_level": level,
        "scenario": scenario,
        "project": report["project"],
        "project_path": report["project_path"],
        "agent": report["agent"],
        "model": report["model"],
        "instance": instance_label,
        "endpoint": report["endpoint"],
        "checks": report["checks"],
        "allow_continue": report["allow_continue"],
    }


def save_benchmark_artifact(artifact: dict[str, Any], output_path: str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(__import__("json").dumps(artifact, indent=2), encoding="utf-8")
    return path


def make_default_artifact_path(
    *,
    root_dir: str,
    scenario: str,
    level: str,
) -> Path:
    safe_scenario = scenario.replace("/", "-").replace("\\", "-").replace(" ", "-")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return Path(root_dir) / "docs" / "unreal-ai-playbook" / "artifacts" / f"{level.lower()}-{safe_scenario}-{timestamp}.json"


def format_preflight_report(report: dict[str, Any]) -> str:
    lines = [
        "=== Benchmark Preflight ===",
        f"Project: {report['project']}",
        f"Project path: {report['project_path']}",
        f"Agent: {report['agent']}",
        f"Model: {report['model']}",
        f"Instance: {report['instance']}",
        f"Endpoint: {report['endpoint']}",
        "",
        "Checks:",
    ]
    for check in report["checks"]:
        mark = "PASS" if check["ok"] else "FAIL"
        lines.append(f"- {check['name']}: {mark} ({check['detail']})")

    lines.extend(
        [
            "",
            f"Allow continue: {'yes' if report['allow_continue'] else 'no'}",
        ]
    )
    return "\n".join(lines)
