import psutil
from pathlib import Path


def find_unreal_editor_processes() -> list[dict]:
    result: list[dict] = []
    try:
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                info = proc.info
                name = info.get("name") or ""
                if "UnrealEditor" not in name:
                    continue
                pid = info.get("pid")
                cmdline = info.get("cmdline") or []
                project_path = find_project_from_cmdline(cmdline)
                result.append(
                    {
                        "pid": pid,
                        "name": name,
                        "cmdline": cmdline,
                        "project_path": project_path,
                    }
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    return result


def get_process_info(pid: int) -> dict | None:
    try:
        proc = psutil.Process(pid)
        mem = proc.memory_info()
        return {
            "pid": pid,
            "name": proc.name(),
            "status": proc.status(),
            "cpu_percent": proc.cpu_percent(),
            "memory_mb": round(mem.rss / (1024 * 1024), 2),
            "create_time": proc.create_time(),
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None


def is_process_alive(pid: int) -> bool:
    try:
        proc = psutil.Process(pid)
        return proc.is_running()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return False


def find_project_from_cmdline(cmdline: list[str]) -> str | None:
    if not cmdline:
        return None
    for arg in cmdline:
        if isinstance(arg, str) and arg.strip().lower().endswith(".uproject"):
            return arg.strip()
    return None


def find_crash_dirs(project_dir: str) -> list[dict]:
    crashes_path = Path(project_dir) / "Saved" / "Crashes"
    if not crashes_path.exists() or not crashes_path.is_dir():
        return []
    entries: list[dict] = []
    try:
        for item in crashes_path.iterdir():
            if item.is_dir():
                try:
                    mtime = item.stat().st_mtime
                except OSError:
                    mtime = 0.0
                entries.append(
                    {
                        "dir_path": str(item),
                        "name": item.name,
                        "modified_time": mtime,
                    }
                )
    except OSError:
        return []
    entries.sort(key=lambda x: x["modified_time"], reverse=True)
    return entries
