from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
from typing import Callable, Literal
import json
import logging
import os
import threading

logger = logging.getLogger(__name__)

STATE_PATH = Path.home() / ".unrealhub" / "state.json"


class Note(BaseModel):
    timestamp: str
    content: str


class ToolCallRecord(BaseModel):
    timestamp: str
    tool_name: str
    success: bool
    duration_ms: float = 0


class InstanceState(BaseModel):
    key: str
    port: int
    url: str
    project_path: str = ""
    project_name: str = ""
    engine_root: str = ""
    pid: int | None = None
    status: Literal["online", "offline"] = "offline"
    last_seen: str = ""
    crash_count: int = 0
    notes: list[Note] = []
    call_history: list[ToolCallRecord] = []


def _normalize_path(p: str) -> str:
    if not p:
        return ""
    return os.path.normcase(os.path.normpath(p))


def make_key(project_path: str, port: int) -> str:
    """Generate stable instance key from project path and port."""
    if project_path:
        name = Path(project_path).stem
        return f"{name}:{port}"
    return f"unknown:{port}"


class StateStore:
    def __init__(self) -> None:
        self._instances: dict[str, InstanceState] = {}
        self._active_key: str = ""
        self._lock = threading.Lock()
        self._on_unregister_callbacks: list[Callable[[str], None]] = []
        self._load()

    def on_unregister(self, callback: Callable[[str], None]) -> None:
        self._on_unregister_callbacks.append(callback)

    # ------------------------------------------------------------------
    # Resolve: fuzzy lookup  exact key > port > project_name
    # ------------------------------------------------------------------

    def _resolve(self, identifier: str) -> str | None:
        if not identifier:
            return None
        with self._lock:
            if identifier in self._instances:
                return identifier
            try:
                port_num = int(identifier)
                for key, inst in self._instances.items():
                    if inst.port == port_num:
                        return key
            except ValueError:
                pass
            id_lower = identifier.lower()
            for key, inst in self._instances.items():
                if inst.project_name and inst.project_name.lower() == id_lower:
                    return key
            return None

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _load(self) -> None:
        if not STATE_PATH.exists():
            return
        try:
            data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
            if "next_id" in data:
                self._migrate_v1_to_v2(data)
            else:
                self._load_v2(data)
        except (json.JSONDecodeError, Exception):
            logger.debug("Failed to load state.json", exc_info=True)

    def _load_v2(self, data: dict) -> None:
        self._instances = {
            k: InstanceState.model_validate(v)
            for k, v in data.get("instances", {}).items()
        }
        self._active_key = data.get("active_key", "")

    def _migrate_v1_to_v2(self, data: dict) -> None:
        old_instances = data.get("instances", {})
        old_active = data.get("active_instance_id", "")
        new_active = ""

        merged: dict[str, dict] = {}
        for auto_id, raw in old_instances.items():
            project_path = raw.get("project_path", "")
            port = raw.get("port", 0)
            if not port:
                continue
            key = make_key(project_path, port)
            existing = merged.get(key)
            if existing and (existing.get("last_seen", "") >= raw.get("last_seen", "")):
                continue
            raw["key"] = key
            raw["project_name"] = Path(project_path).stem if project_path else ""
            for field in ("auto_id", "alias", "first_seen", "last_health_check", "metrics"):
                raw.pop(field, None)
            if raw.get("status") in ("crashed", "starting"):
                raw["status"] = "offline"
            merged[key] = raw
            if auto_id == old_active:
                new_active = key

        self._instances = {
            k: InstanceState.model_validate(v) for k, v in merged.items()
        }
        self._active_key = new_active
        self.save()
        logger.info("Migrated state.json v1->v2: %d instances", len(self._instances))

    def save(self) -> None:
        with self._lock:
            data = {
                "instances": {k: v.model_dump() for k, v in self._instances.items()},
                "active_key": self._active_key,
            }
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        STATE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")

    # ------------------------------------------------------------------
    # Core: upsert
    # ------------------------------------------------------------------

    def upsert(
        self,
        port: int,
        project_path: str = "",
        *,
        url: str = "",
        engine_root: str = "",
        pid: int | None = None,
        status: Literal["online", "offline"] = "online",
    ) -> InstanceState:
        """Insert or update an instance. Key is derived from (project_path, port).

        port=0 is a valid sentinel for "process running but no MCP endpoint".
        When a real port is later discovered for the same project, the port=0
        entry is automatically upgraded.
        """
        key = make_key(project_path, port)
        now = datetime.now().isoformat()
        if not url:
            url = f"http://localhost:{port}/mcp" if port else ""
        project_name = Path(project_path).stem if project_path else ""

        upgraded_from: str | None = None

        with self._lock:
            # Upgrade path 1: unknown:{port} → ProjectName:{port}
            unknown_key = f"unknown:{port}"
            if project_path and key != unknown_key and unknown_key in self._instances:
                old = self._instances.pop(unknown_key)
                self._instances[key] = InstanceState(
                    key=key, port=port, url=url,
                    project_path=project_path, project_name=project_name,
                    engine_root=engine_root or old.engine_root,
                    pid=pid if pid is not None else old.pid,
                    status=status, last_seen=now,
                    crash_count=old.crash_count,
                    notes=old.notes, call_history=old.call_history,
                )
                if self._active_key == unknown_key:
                    self._active_key = key
                upgraded_from = unknown_key

            # Upgrade path 2: ProjectName:0 → ProjectName:{port}
            elif port > 0 and project_name and f"{project_name}:0" in self._instances and key != f"{project_name}:0":
                no_mcp_key = f"{project_name}:0"
                old = self._instances.pop(no_mcp_key)
                self._instances[key] = InstanceState(
                    key=key, port=port, url=url,
                    project_path=project_path or old.project_path,
                    project_name=project_name or old.project_name,
                    engine_root=engine_root or old.engine_root,
                    pid=pid if pid is not None else old.pid,
                    status=status, last_seen=now,
                    crash_count=old.crash_count,
                    notes=old.notes, call_history=old.call_history,
                )
                if self._active_key == no_mcp_key:
                    self._active_key = key
                upgraded_from = no_mcp_key

            elif key in self._instances:
                inst = self._instances[key]
                inst.status = status
                inst.last_seen = now
                inst.url = url
                if project_path:
                    inst.project_path = project_path
                    inst.project_name = project_name
                if engine_root:
                    inst.engine_root = engine_root
                if pid is not None:
                    inst.pid = pid
            else:
                self._instances[key] = InstanceState(
                    key=key, port=port, url=url,
                    project_path=project_path, project_name=project_name,
                    engine_root=engine_root, pid=pid,
                    status=status, last_seen=now,
                )

            if status == "online":
                for other_key, other_inst in self._instances.items():
                    if other_key != key and other_inst.port == port and other_inst.status == "online":
                        other_inst.status = "offline"
                        other_inst.last_seen = now

            current_active = self._instances.get(self._active_key)
            if not current_active or current_active.status != "online":
                if status == "online":
                    self._active_key = key

            result = self._instances[key]

        if upgraded_from:
            self._fire_unregister(upgraded_from)
        self.save()
        return result

    # ------------------------------------------------------------------
    # Instance management
    # ------------------------------------------------------------------

    def unregister_instance(self, identifier: str) -> bool:
        resolved = self._resolve(identifier)
        if resolved is None:
            return False
        with self._lock:
            del self._instances[resolved]
            if self._active_key == resolved:
                self._active_key = next(iter(self._instances), "") if self._instances else ""
        self.save()
        self._fire_unregister(resolved)
        return True

    def _fire_unregister(self, key: str) -> None:
        for cb in self._on_unregister_callbacks:
            try:
                cb(key)
            except Exception:
                logger.debug("on_unregister callback error for %s", key, exc_info=True)

    def get_instance(self, identifier: str) -> InstanceState | None:
        resolved = self._resolve(identifier)
        if resolved is None:
            return None
        with self._lock:
            return self._instances.get(resolved)

    def get_active_instance(self) -> InstanceState | None:
        with self._lock:
            inst = self._instances.get(self._active_key)
            if inst and inst.status == "online":
                return inst
            for key, candidate in self._instances.items():
                if candidate.status == "online":
                    self._active_key = key
                    return candidate
            return inst

    def set_active(self, identifier: str) -> bool:
        resolved = self._resolve(identifier)
        if resolved is None:
            return False
        with self._lock:
            self._active_key = resolved
        self.save()
        return True

    def list_instances(self) -> list[InstanceState]:
        with self._lock:
            return list(self._instances.values())

    def list_instances_summary(self) -> str:
        with self._lock:
            if not self._instances:
                return "  (no instances)"

            online = sum(1 for i in self._instances.values() if i.status == "online")
            lines = [f"Instances ({len(self._instances)} total, {online} online):"]

            for inst in self._instances.values():
                marker = "* " if inst.key == self._active_key else "  "
                pid_str = f"PID={inst.pid}" if inst.pid else "PID=?"
                no_mcp = " [NO MCP]" if inst.port == 0 else ""
                line = f"  {marker}{inst.key} {inst.status.upper()}  {pid_str}{no_mcp}"
                lines.append(line)

                if inst.project_path:
                    lines.append(f"      Project: {inst.project_path}")
                if inst.last_seen:
                    extra = f" (crashed x{inst.crash_count})" if inst.crash_count else ""
                    lines.append(f"      Last seen: {inst.last_seen}{extra}")

            return "\n".join(lines)

    # ------------------------------------------------------------------
    # Lookup helpers
    # ------------------------------------------------------------------

    def find_by_project_path(self, project_path: str) -> list[InstanceState]:
        norm = _normalize_path(project_path)
        if not norm:
            return []
        with self._lock:
            return [
                inst for inst in self._instances.values()
                if _normalize_path(inst.project_path) == norm
            ]

    def find_by_port(self, port: int) -> list[InstanceState]:
        with self._lock:
            return [inst for inst in self._instances.values() if inst.port == port]

    # ------------------------------------------------------------------
    # Status updates
    # ------------------------------------------------------------------

    def update_status(
        self,
        identifier: str,
        status: Literal["online", "offline"],
        pid: int | None = None,
    ) -> None:
        resolved = self._resolve(identifier)
        if resolved is None:
            return
        with self._lock:
            inst = self._instances[resolved]
            inst.status = status
            inst.last_seen = datetime.now().isoformat()
            if pid is not None:
                inst.pid = pid
            if status == "offline" and self._active_key == resolved:
                for key, candidate in self._instances.items():
                    if candidate.status == "online":
                        self._active_key = key
                        break
        self.save()

    def increment_crash_count(self, identifier: str) -> None:
        resolved = self._resolve(identifier)
        if resolved is None:
            return
        with self._lock:
            self._instances[resolved].crash_count += 1
            self._instances[resolved].status = "offline"
        self.save()

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def cleanup(self, max_age_hours: float = 1.0) -> list[str]:
        """Remove offline instances older than max_age_hours."""
        now = datetime.now()
        removed: list[str] = []
        with self._lock:
            to_remove: list[str] = []
            for key, inst in self._instances.items():
                if inst.status == "online":
                    continue
                if not inst.last_seen:
                    continue
                try:
                    last = datetime.fromisoformat(inst.last_seen)
                    if (now - last).total_seconds() > max_age_hours * 3600:
                        to_remove.append(key)
                except ValueError:
                    pass
            for key in to_remove:
                del self._instances[key]
                if self._active_key == key:
                    self._active_key = next(iter(self._instances), "") if self._instances else ""
                removed.append(key)
        if removed:
            self.save()
            for key in removed:
                self._fire_unregister(key)
            logger.info("Cleaned up stale instances: %s", removed)
        return removed

    # ------------------------------------------------------------------
    # Notes & call history
    # ------------------------------------------------------------------

    def add_note(self, identifier: str, content: str) -> None:
        resolved = self._resolve(identifier)
        if resolved is None:
            return
        note = Note(timestamp=datetime.now().isoformat(), content=content)
        with self._lock:
            self._instances[resolved].notes.append(note)
        self.save()

    def get_notes(self, identifier: str) -> list[Note]:
        resolved = self._resolve(identifier)
        if resolved is None:
            return []
        with self._lock:
            return list(self._instances[resolved].notes)

    def record_tool_call(
        self,
        identifier: str,
        tool_name: str,
        success: bool,
        duration_ms: float = 0,
    ) -> None:
        resolved = self._resolve(identifier)
        if resolved is None:
            return
        record = ToolCallRecord(
            timestamp=datetime.now().isoformat(),
            tool_name=tool_name,
            success=success,
            duration_ms=duration_ms,
        )
        with self._lock:
            self._instances[resolved].call_history.append(record)
        self.save()

    def get_call_history(
        self, identifier: str, limit: int = 50
    ) -> list[ToolCallRecord]:
        resolved = self._resolve(identifier)
        if resolved is None:
            return []
        with self._lock:
            history = self._instances[resolved].call_history
            return list(history[-limit:])
