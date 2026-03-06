from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
from typing import Literal
import json
import threading

STATE_PATH = Path.home() / ".unrealhub" / "state.json"


class Note(BaseModel):
    timestamp: str
    content: str


class ToolCallRecord(BaseModel):
    timestamp: str
    tool_name: str
    success: bool
    duration_ms: float = 0


class ProcessMetrics(BaseModel):
    cpu_percent: float = 0
    memory_mb: float = 0
    last_updated: str = ""


class InstanceState(BaseModel):
    auto_id: str
    alias: str | None = None
    url: str
    port: int
    project_path: str = ""
    engine_root: str = ""
    pid: int | None = None
    status: Literal["online", "offline", "crashed", "starting"] = "offline"
    first_seen: str = ""
    last_seen: str = ""
    last_health_check: str = ""
    crash_count: int = 0
    notes: list[Note] = []
    call_history: list[ToolCallRecord] = []
    metrics: ProcessMetrics = ProcessMetrics()


class StateStore:
    def __init__(self):
        self._instances: dict[str, InstanceState] = {}
        self._active_instance_id: str = ""
        self._next_id: int = 1
        self._lock = threading.Lock()
        self._load()

    def _resolve(self, identifier: str) -> str | None:
        with self._lock:
            if identifier in self._instances:
                return identifier
            for auto_id, inst in self._instances.items():
                if inst.alias == identifier:
                    return auto_id
            return None

    def _load(self) -> None:
        if STATE_PATH.exists():
            try:
                data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
                self._instances = {
                    k: InstanceState.model_validate(v)
                    for k, v in data.get("instances", {}).items()
                }
                self._active_instance_id = data.get("active_instance_id", "")
                loaded_next = data.get("next_id", 1)
                max_id = 0
                for auto_id in self._instances:
                    if auto_id.startswith("ue") and auto_id[2:].isdigit():
                        max_id = max(max_id, int(auto_id[2:]))
                self._next_id = max(loaded_next, max_id + 1)
            except (json.JSONDecodeError, Exception):
                pass

    def save(self) -> None:
        with self._lock:
            data = {
                "instances": {k: v.model_dump() for k, v in self._instances.items()},
                "active_instance_id": self._active_instance_id,
                "next_id": self._next_id,
            }
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        STATE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def register_instance(
        self,
        url: str,
        port: int,
        project_path: str = "",
        engine_root: str = "",
        pid: int | None = None,
    ) -> InstanceState:
        now = datetime.now().isoformat()
        auto_id = f"ue{self._next_id}"
        self._next_id += 1
        instance = InstanceState(
            auto_id=auto_id,
            url=url,
            port=port,
            project_path=project_path,
            engine_root=engine_root,
            pid=pid,
            status="online" if pid else "offline",
            first_seen=now,
            last_seen=now,
            last_health_check=now,
        )
        with self._lock:
            self._instances[auto_id] = instance
            if not self._active_instance_id:
                self._active_instance_id = auto_id
        self.save()
        return instance

    def unregister_instance(self, instance_id: str) -> bool:
        resolved = self._resolve(instance_id)
        if resolved is None:
            return False
        with self._lock:
            del self._instances[resolved]
            if self._active_instance_id == resolved:
                self._active_instance_id = (
                    next(iter(self._instances), "") if self._instances else ""
                )
        self.save()
        return True

    def get_instance(self, identifier: str) -> InstanceState | None:
        resolved = self._resolve(identifier)
        if resolved is None:
            return None
        with self._lock:
            return self._instances.get(resolved)

    def get_active_instance(self) -> InstanceState | None:
        with self._lock:
            if not self._active_instance_id:
                return None
            return self._instances.get(self._active_instance_id)

    def set_active(self, identifier: str) -> bool:
        resolved = self._resolve(identifier)
        if resolved is None:
            return False
        with self._lock:
            self._active_instance_id = resolved
        self.save()
        return True

    def set_alias(self, identifier: str, alias: str) -> bool:
        resolved = self._resolve(identifier)
        if resolved is None:
            return False
        with self._lock:
            self._instances[resolved].alias = alias or None
        self.save()
        return True

    def list_instances(self) -> list[InstanceState]:
        with self._lock:
            return list(self._instances.values())

    def list_instances_summary(self) -> str:
        with self._lock:
            lines = []
            for inst in self._instances.values():
                marker = " *" if inst.auto_id == self._active_instance_id else ""
                name = inst.alias or inst.auto_id
                lines.append(f"  {name} ({inst.auto_id}): {inst.status}{marker}")
            return "\n".join(lines) if lines else "  (no instances)"

    def update_status(
        self, instance_id: str, status: str, pid: int | None = None
    ) -> None:
        resolved = self._resolve(instance_id)
        if resolved is None:
            return
        with self._lock:
            inst = self._instances[resolved]
            inst.status = status
            inst.last_seen = datetime.now().isoformat()
            if pid is not None:
                inst.pid = pid
        self.save()

    def record_health_check(self, instance_id: str, healthy: bool) -> None:
        resolved = self._resolve(instance_id)
        if resolved is None:
            return
        with self._lock:
            inst = self._instances[resolved]
            inst.last_health_check = datetime.now().isoformat()
            inst.status = "online" if healthy else "offline"
        self.save()

    def increment_crash_count(self, instance_id: str) -> None:
        resolved = self._resolve(instance_id)
        if resolved is None:
            return
        with self._lock:
            self._instances[resolved].crash_count += 1
            self._instances[resolved].status = "crashed"
        self.save()

    def add_note(self, instance_id: str, content: str) -> None:
        resolved = self._resolve(instance_id)
        if resolved is None:
            return
        note = Note(
            timestamp=datetime.now().isoformat(),
            content=content,
        )
        with self._lock:
            self._instances[resolved].notes.append(note)
        self.save()

    def get_notes(self, instance_id: str) -> list[Note]:
        resolved = self._resolve(instance_id)
        if resolved is None:
            return []
        with self._lock:
            return list(self._instances[resolved].notes)

    def record_tool_call(
        self,
        instance_id: str,
        tool_name: str,
        success: bool,
        duration_ms: float = 0,
    ) -> None:
        resolved = self._resolve(instance_id)
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
        self, instance_id: str, limit: int = 50
    ) -> list[ToolCallRecord]:
        resolved = self._resolve(instance_id)
        if resolved is None:
            return []
        with self._lock:
            history = self._instances[resolved].call_history
            return list(history[-limit:])
