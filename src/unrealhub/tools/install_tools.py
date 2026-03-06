import asyncio
import io
import json
import logging
import shutil
import zipfile
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP

from unrealhub.config import CONFIG_DIR

logger = logging.getLogger(__name__)

CACHE_DIR = CONFIG_DIR / "cache"


async def _download_plugin_zip(repo_url: str) -> Path | None:
    """Download a zip from repo_url and extract it. Returns extracted dir or None."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = CACHE_DIR / "RemoteMCP-latest.zip"

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0), follow_redirects=True) as client:
            resp = await client.get(repo_url)
            resp.raise_for_status()
            zip_path.write_bytes(resp.content)
    except Exception as e:
        logger.error("Failed to download plugin zip: %s", e)
        return None

    extract_dir = CACHE_DIR / "RemoteMCP-extracted"
    if extract_dir.exists():
        shutil.rmtree(extract_dir, ignore_errors=True)

    try:
        with zipfile.ZipFile(io.BytesIO(zip_path.read_bytes())) as zf:
            zf.extractall(extract_dir)
    except Exception as e:
        logger.error("Failed to extract plugin zip: %s", e)
        return None

    for child in extract_dir.iterdir():
        if child.is_dir() and (child / "RemoteMCP.uplugin").exists():
            return child

    return None


def _find_local_plugin(config, project_dir: Path) -> str | None:
    """Search local paths for an existing RemoteMCP source directory."""
    cache_path = config.get_plugin_cache()
    candidates = [
        Path(cache_path) if cache_path else None,
        Path(__file__).resolve().parents[4] / "RemoteMCP",
        project_dir / "Plugins" / "RemoteMCP",
    ]
    for c in candidates:
        if c and c.is_dir() and (c / "RemoteMCP.uplugin").exists():
            return str(c)
    return None


def register_install_tools(mcp: FastMCP, get_config) -> None:

    @mcp.tool()
    async def install_plugin(
        target_project: str = "",
        plugin_source: str = "",
    ) -> str:
        """Install the RemoteMCP plugin to a UE project.

        target_project: Path to .uproject file. Defaults to active project.
        plugin_source: Path to local RemoteMCP directory. If empty, auto-detects
                       locally first; if not found, downloads from configured GitHub repo.
        """
        config = get_config()

        if not target_project:
            proj = config.get_active_project()
            if not proj:
                return (
                    "No target project specified and no active project configured. "
                    "Call setup_project() first."
                )
            target_project = proj.uproject_path

        target_path = Path(target_project)
        if not target_path.exists():
            return f".uproject not found: {target_project}"

        project_dir = target_path.parent
        plugins_dir = project_dir / "Plugins"
        dest_dir = plugins_dir / "RemoteMCP"

        if dest_dir.exists() and (dest_dir / "RemoteMCP.uplugin").exists():
            return (
                f"RemoteMCP already installed at: {dest_dir}\n"
                "Use check_plugin_status() to verify."
            )

        # --- Tier 1: user-provided path ---
        if plugin_source:
            source_path = Path(plugin_source)
            if not (source_path / "RemoteMCP.uplugin").exists():
                return f"Invalid plugin source (no RemoteMCP.uplugin): {plugin_source}"
            return _copy_and_enable(source_path, dest_dir, target_path)

        # --- Tier 2: local auto-detect (sibling dir / cache) ---
        local = _find_local_plugin(config, project_dir)
        if local:
            return _copy_and_enable(Path(local), dest_dir, target_path)

        # --- Tier 3: download from GitHub ---
        repo_url = config.get_plugin_repo()
        download_msg = f"Downloading RemoteMCP from:\n  {repo_url}\n"

        extracted = await _download_plugin_zip(repo_url)
        if not extracted:
            return (
                f"{download_msg}"
                "Download FAILED. Check your network or use set_plugin_source() "
                "to configure a different repo URL or local path."
            )

        config.set_plugin_cache(str(extracted))
        result = _copy_and_enable(extracted, dest_dir, target_path)
        return f"{download_msg}Download OK.\n\n{result}"

    @mcp.tool()
    async def set_plugin_source(repo_url: str = "", local_path: str = "") -> str:
        """Configure the RemoteMCP plugin source.

        repo_url: GitHub zip download URL (leave empty to keep current).
        local_path: Local RemoteMCP directory path (highest priority when installing).

        Examples:
          set_plugin_source(repo_url="https://github.com/user/repo/archive/refs/heads/main.zip")
          set_plugin_source(local_path="D:/Projects/RemoteMCP")
        """
        config = get_config()
        lines = []

        if repo_url:
            config.set_plugin_repo(repo_url)
            lines.append(f"Plugin repo URL set to: {repo_url}")

        if local_path:
            p = Path(local_path)
            if not p.is_dir() or not (p / "RemoteMCP.uplugin").exists():
                return f"Invalid local path (no RemoteMCP.uplugin): {local_path}"
            config.set_plugin_cache(local_path)
            lines.append(f"Plugin local cache set to: {local_path}")

        if not lines:
            current_repo = config.get_plugin_repo()
            current_cache = config.get_plugin_cache()
            return (
                f"Current plugin source config:\n"
                f"  Repo URL: {current_repo}\n"
                f"  Local cache: {current_cache or '(none)'}"
            )

        return "\n".join(lines)

    @mcp.tool()
    async def enable_plugin(target_project: str = "") -> str:
        """Enable RemoteMCP and PythonScriptPlugin in a .uproject file."""
        config = get_config()
        if not target_project:
            proj = config.get_active_project()
            if not proj:
                return "No project configured."
            target_project = proj.uproject_path
        return _enable_plugins_in_uproject(target_project)

    @mcp.tool()
    async def check_plugin_status(target_project: str = "") -> str:
        """Check if RemoteMCP plugin is installed and enabled."""
        config = get_config()
        if not target_project:
            proj = config.get_active_project()
            if not proj:
                return "No project configured."
            target_project = proj.uproject_path

        target_path = Path(target_project)
        project_dir = target_path.parent
        plugin_dir = project_dir / "Plugins" / "RemoteMCP"

        lines = [f"Project: {target_project}"]

        if plugin_dir.exists() and (plugin_dir / "RemoteMCP.uplugin").exists():
            lines.append("Plugin directory: INSTALLED")
        else:
            lines.append("Plugin directory: NOT FOUND")
            lines.append("  Run install_plugin() to install.")
            return "\n".join(lines)

        try:
            with open(target_project, "r", encoding="utf-8") as f:
                data = json.load(f)
            plugins_map = {
                p.get("Name"): p.get("Enabled", False)
                for p in data.get("Plugins", [])
                if "Name" in p
            }
            for name in ["RemoteMCP", "PythonScriptPlugin"]:
                if name in plugins_map:
                    status = "ENABLED" if plugins_map[name] else "DISABLED"
                else:
                    status = "NOT IN .uproject"
                lines.append(f"{name}: {status}")
        except Exception as e:
            lines.append(f"Error reading .uproject: {e}")

        python_dir = plugin_dir / "Content" / "Python"
        if (python_dir / "Lib" / "site-packages" / "mcp").exists():
            lines.append("Python deps: INSTALLED")
        else:
            lines.append("Python deps: NOT FOUND (run install_python_deps)")

        return "\n".join(lines)

    @mcp.tool()
    async def install_python_deps(target_project: str = "") -> str:
        """Install Python dependencies for RemoteMCP plugin using uv."""
        config = get_config()
        if not target_project:
            proj = config.get_active_project()
            if not proj:
                return "No project configured."
            target_project = proj.uproject_path

        python_dir = (
            Path(target_project).parent / "Plugins" / "RemoteMCP" / "Content" / "Python"
        )
        if not python_dir.exists():
            return "RemoteMCP Python directory not found. Is the plugin installed?"

        env_bat = python_dir / "env.bat"
        if not env_bat.exists():
            return "env.bat not found. Install dependencies manually."

        try:
            proc = await asyncio.create_subprocess_exec(
                "cmd", "/c", str(env_bat),
                cwd=str(python_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )
            output, _ = await asyncio.wait_for(proc.communicate(), timeout=120)
            text = output.decode("utf-8", errors="replace")
            return f"Exit code: {proc.returncode}\n{text}"
        except asyncio.TimeoutError:
            return "install_python_deps timed out after 120 seconds."
        except Exception as e:
            logger.exception("install_python_deps failed")
            return f"Failed to run env.bat: {e}"


def _copy_and_enable(source: Path, dest: Path, uproject_path: Path) -> str:
    """Copy plugin source to dest and enable in .uproject."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copytree(
            str(source), str(dest),
            ignore=shutil.ignore_patterns(
                "__pycache__", "*.pyc", ".git", "Intermediate", "Binaries",
            ),
        )
    except Exception as e:
        logger.exception("Plugin copy failed")
        return f"Failed to copy plugin: {e}"

    lines = [f"RemoteMCP installed to: {dest}"]
    lines.append(_enable_plugins_in_uproject(str(uproject_path)))
    lines.append("\nNext steps:")
    lines.append("1. Run compile_project() to build")
    lines.append("2. Run launch_editor() to start the editor")
    return "\n".join(lines)


def _enable_plugins_in_uproject(uproject_path: str) -> str:
    try:
        with open(uproject_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        plugins = data.setdefault("Plugins", [])
        plugin_map = {p["Name"]: p for p in plugins if "Name" in p}

        changed = False
        for name in ["PythonScriptPlugin", "RemoteMCP"]:
            if name in plugin_map:
                if not plugin_map[name].get("Enabled", False):
                    plugin_map[name]["Enabled"] = True
                    changed = True
            else:
                plugins.append({"Name": name, "Enabled": True})
                changed = True

        if changed:
            with open(uproject_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return "Plugins enabled in .uproject: PythonScriptPlugin, RemoteMCP"
        return "Plugins already enabled in .uproject."
    except Exception as e:
        logger.exception("_enable_plugins_in_uproject failed")
        return f"Failed to update .uproject: {e}"
