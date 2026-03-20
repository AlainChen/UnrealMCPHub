from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

_SKILL_PATH = Path(__file__).resolve().parents[3] / "skills" / "use-unrealhub" / "SKILL.md"

_PART_RE = re.compile(r"^## Part \d+:", re.MULTILINE)

_TOPIC_ALIASES: dict[str, list[str]] = {
    "workflow": ["workflow", "core", "工作流", "决策"],
    "compile": ["compile", "build", "编译", "ubt"],
    "launch": ["launch", "editor", "启动", "弹窗", "popup"],
    "pie": ["pie", "test", "play", "测试"],
    "nav": ["nav", "navmesh", "寻路", "navigation"],
    "level": ["level", "关卡", "场景", "spawn"],
    "rules": ["rules", "行为", "准则", "guidelines"],
    "slate": ["slate", "ui", "窗口", "widget tree"],
    "umg": ["umg", "widget", "hud", "umg widget"],
}

_PART_TOPIC_MAP: dict[int, str] = {
    1: "workflow",
    2: "compile",
    3: "launch",
    4: "pie",
    5: "nav",
    6: "level",
    7: "rules",
    8: "slate",
    9: "umg",
}


def _load_skill() -> str:
    try:
        return _SKILL_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _split_parts(text: str) -> dict[int, str]:
    """Split SKILL.md into {part_number: content} using '## Part N:' markers."""
    matches = list(_PART_RE.finditer(text))
    if not matches:
        return {}

    parts: dict[int, str] = {}
    for i, m in enumerate(matches):
        header_line = text[m.start(): text.index("\n", m.start())]
        num_match = re.search(r"Part (\d+):", header_line)
        if not num_match:
            continue
        num = int(num_match.group(1))
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        parts[num] = text[start:end].rstrip()
    return parts


def _resolve_topic(query: str) -> str | None:
    q = query.strip().lower()
    if not q:
        return None
    for canonical, aliases in _TOPIC_ALIASES.items():
        if q in aliases or q == canonical:
            return canonical
    for canonical, aliases in _TOPIC_ALIASES.items():
        if any(q in alias for alias in aliases) or q in canonical:
            return canonical
    return None


def _build_topic_list() -> str:
    lines = ["Available topics:"]
    for part_num in sorted(_PART_TOPIC_MAP):
        topic = _PART_TOPIC_MAP[part_num]
        aliases = _TOPIC_ALIASES.get(topic, [])
        alias_str = ", ".join(f'"{a}"' for a in aliases[:3])
        lines.append(f"  {topic:10s} (Part {part_num}, aliases: {alias_str})")
    lines.append('  full       (return the complete guide)')
    return "\n".join(lines)


def register_help_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def help(topic: str = "") -> str:
        """Get the UnrealMCPHub usage guide.

        topic: specific section to retrieve.
          '' (default) — overview (Part 1: core workflow) + available topics.
          'compile'    — Part 2: build & compile strategy.
          'launch'     — Part 3: editor launch & popup handling.
          'pie'        — Part 4: PIE testing.
          'nav'        — Part 5: AI navigation & NavMesh.
          'level'      — Part 6: level building.
          'rules'      — Part 7: behavioral guidelines.
          'slate'      — Part 8: Slate UI manipulation.
          'umg'        — Part 9: UMG widget creation.
          'full'       — complete guide (all parts).

        Aliases are supported: 'build'='compile', 'editor'='launch',
        'test'='pie', 'ui'='slate', 'widget'='umg', etc.
        """
        raw = _load_skill()
        if not raw:
            return "SKILL.md not found. The guide file may be missing from the installation."

        if topic.strip().lower() == "full":
            frontmatter_end = raw.find("\n---\n", raw.find("---") + 3)
            if frontmatter_end > 0:
                return raw[frontmatter_end + 5:].strip()
            return raw

        parts = _split_parts(raw)
        if not parts:
            return raw

        resolved = _resolve_topic(topic)

        if resolved is None:
            part1 = parts.get(1, "")
            return f"{part1}\n\n---\n\n{_build_topic_list()}"

        for part_num, canonical in _PART_TOPIC_MAP.items():
            if canonical == resolved:
                content = parts.get(part_num)
                if content:
                    return content
                return f"Topic '{topic}' matched Part {part_num} but content was empty."

        return f"Unknown topic '{topic}'.\n\n{_build_topic_list()}"
