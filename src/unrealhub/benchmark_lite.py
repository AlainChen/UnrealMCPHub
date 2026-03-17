from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from unrealhub.config import ProjectConfig
from unrealhub.preflight import run_benchmark_preflight
from unrealhub.state import StateStore
from unrealhub.ue_client import UEMCPClient


async def _list_top_level_tools(url: str) -> list[str]:
    client = UEMCPClient(url, timeout_connect=3.0, timeout_read=8.0)
    tools = await client.list_tools()
    return [tool["name"] for tool in tools]


async def _list_domains_and_counts(url: str) -> tuple[list[str], dict[str, int]]:
    client = UEMCPClient(url, timeout_connect=3.0, timeout_read=8.0)
    result = await client.call_tool("get_dispatch", {})
    if not result.get("success") or not result.get("content"):
        return [], {}

    payload = json.loads(result["content"][0]["text"])
    domains = payload.get("domains", [])
    counts: dict[str, int] = {}
    for domain in domains:
        domain_result = await client.call_tool("get_dispatch", {"domain": domain})
        if not domain_result.get("success") or not domain_result.get("content"):
            counts[domain] = 0
            continue
        domain_payload = json.loads(domain_result["content"][0]["text"])
        counts[domain] = len(domain_payload.get("tools", []))
    return domains, counts


def make_benchmark_lite_artifact_path(
    *,
    root_dir: str,
    level: str,
    scenario: str,
) -> Path:
    safe_scenario = scenario.replace("/", "-").replace("\\", "-").replace(" ", "-")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return Path(root_dir) / "docs" / "unreal-ai-playbook" / "artifacts" / f"{level.lower()}-{safe_scenario}-lite-{timestamp}.json"


def save_benchmark_lite_artifact(artifact: dict[str, Any], output_path: str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    return path


async def run_benchmark_lite(
    *,
    config: ProjectConfig,
    state: StateStore,
    level: str = "L0",
    scenario: str = "smoke-connectivity-v1",
    agent: str = "",
    model: str = "",
) -> dict[str, Any]:
    preflight = await run_benchmark_preflight(
        config=config,
        state=state,
        agent=agent,
        model=model,
    )

    artifact: dict[str, Any] = {
        "artifact_type": "benchmark_lite",
        "generated_at": datetime.now().isoformat(),
        "benchmark_level": level,
        "scenario": scenario,
        "agent": preflight["agent"],
        "model": preflight["model"],
        "project": preflight["project"],
        "project_path": preflight["project_path"],
        "instance": preflight["instance"],
        "endpoint": preflight["endpoint"],
        "preflight": preflight,
        "top_level_tools": [],
        "domains": [],
        "domain_tool_counts": {},
        "ready_for_next_level": False,
        "recommended_next_level": "L0",
    }

    if not preflight["allow_continue"]:
        return artifact

    proj = config.get_active_project()
    if proj is None:
        return artifact

    url = f"http://127.0.0.1:{proj.mcp_port}/mcp"
    artifact["top_level_tools"] = await _list_top_level_tools(url)
    domains, counts = await _list_domains_and_counts(url)
    artifact["domains"] = domains
    artifact["domain_tool_counts"] = counts
    artifact["ready_for_next_level"] = bool(domains) and bool(artifact["top_level_tools"])
    artifact["recommended_next_level"] = "L1" if level == "L0" and artifact["ready_for_next_level"] else level
    return artifact


def format_benchmark_lite_report(artifact: dict[str, Any]) -> str:
    lines = [
        "=== Benchmark Lite ===",
        f"Level: {artifact['benchmark_level']}",
        f"Scenario: {artifact['scenario']}",
        f"Project: {artifact['project']}",
        f"Agent: {artifact['agent']}",
        f"Model: {artifact['model']}",
        f"Ready for next level: {'yes' if artifact['ready_for_next_level'] else 'no'}",
        f"Recommended next level: {artifact['recommended_next_level']}",
        "",
        "Top-level tools:",
    ]
    if artifact["top_level_tools"]:
        lines.extend([f"- {name}" for name in artifact["top_level_tools"]])
    else:
        lines.append("- none")

    lines.extend(["", "Domain tool counts:"])
    if artifact["domain_tool_counts"]:
        for domain, count in artifact["domain_tool_counts"].items():
            lines.append(f"- {domain}: {count}")
    else:
        lines.append("- none")

    return "\n".join(lines)
