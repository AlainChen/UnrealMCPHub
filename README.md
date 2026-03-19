# UnrealMCPHub

Central management platform for Unreal Engine MCP instances — bridge between AI agents and UE across the full development lifecycle.

Works with **[RemoteMCP](https://github.com/blackplume233/UnrealRemoteMCP)** (UE Editor plugin that exposes engine capabilities via MCP protocol). The Hub manages everything around it: install the plugin, compile, launch the editor, detect crashes, and transparently proxy all tool calls — so the AI agent only needs one MCP endpoint.

```
AI Agent ──► UnrealMCPHub ──► UE Editor + RemoteMCP plugin
              (this repo)       (blackplume233/UnrealRemoteMCP)
```

> **RemoteMCP** runs **inside** UE Editor and provides 17+ tools across 6 domains (level, blueprint, umg, edgraph, behaviortree, slate).
> **UnrealMCPHub** runs **outside** UE Editor and can compile, launch, monitor, and proxy — even when UE is not running.

## How It Works With UnrealRemoteMCP

`UnrealMCPHub` and `UnrealRemoteMCP` are complementary layers, not competing projects.

- **UnrealRemoteMCP** lives inside Unreal Editor and exposes engine-facing tools.
- **UnrealMCPHub** lives outside Unreal Editor and manages the development lifecycle around those tools.

In practice, the flow looks like this:

1. The AI client connects to `UnrealMCPHub`.
2. The Hub configures the Unreal project, installs or verifies the plugin, compiles, and launches the editor when needed.
3. Once the editor is ready, the Hub forwards UE-facing requests to `UnrealRemoteMCP`.
4. `UnrealRemoteMCP` executes the actual in-editor work and returns results through the Hub.

This separation is the main reason the Hub is useful in production-like workflows:

- `UnrealRemoteMCP` handles **tool execution inside UE**
- `UnrealMCPHub` handles **project setup, process management, recovery, discovery, and routing**

In short: `UnrealRemoteMCP` is the in-editor capability layer, while `UnrealMCPHub` is the control plane around it.

## About This Fork

This fork keeps upstream UnrealMCPHub as the base, but adds a workflow and benchmark experimentation layer around it.

Compared with upstream, this fork currently adds:

- **Team workflow docs** under [`docs/unreal-ai-playbook/`](./docs/unreal-ai-playbook/) for sandbox rules, review flow, benchmark planning, and research notes
- **A project-facing wrapper skill** under [`skills/team-unreal-workflow/`](./skills/team-unreal-workflow/) that narrows `use-unrealhub` into a safer day-to-day workflow
- **A benchmark ladder** with lighter scenarios before the heavyweight `vampire-survivors-v1` benchmark
- **Local experiment helpers** on the `codex/lab` branch for source-run and environment troubleshooting

Recommended branch roles in this fork:

- `main`: the stable fork baseline that tracks upstream plus fork-approved documentation and workflow changes
- `codex/lab`: the active working branch for experiments, benchmark tooling, validation utilities, and local integration work
- `codex/team-workflow`: the branch that introduced the team workflow and documentation structure; keep it as a historical docs-oriented branch or reuse it only for large workflow-only reorganizations
- `codex/pr-discovery-fallback`: a small upstream-friendly branch reserved for the discovery fallback fix, so it can stay clean and easy to propose upstream

Optional branch:

- `codex/benchmark`: use only if you want a separate branch dedicated to benchmark scenarios or benchmark-only iteration

In short: upstream is the base product, while this fork is organized as a research and workflow-oriented variant for Unreal AI experimentation.

## Fork Sync Strategy

This fork is intended to stay compatible with upstream rather than diverge permanently.

- `main` should stay close to upstream and receive only fork-approved workflow, documentation, and broadly useful improvements.
- `codex/lab` remains the staging branch for research, gym iteration, automation experiments, and docs that are still moving quickly.
- Small, generally useful fixes should be split into focused branches and proposed upstream when practical.
- Fork-specific workflow assets, local evidence handling rules, and Gym research notes can stay in this fork even if they are never proposed upstream.

Recommended sync loop:

1. `fetch upstream`
2. update local `main` from `upstream/main`
3. merge the refreshed `main` back into `codex/lab`
4. carve out small upstream-friendly branches only for changes that are clean and generally reusable

In practice, that means:
- treat this fork as the research/control-plane layer
- treat upstream as the long-term compatibility baseline
- avoid mixing local artifact decisions or team-specific workflow rules into upstream-facing changes

## Benchmark Status

This fork has now driven a `vampire-survivors-v1` style benchmark through a full validation ladder:

- `L0` connectivity and preflight checks
- `L1` sandbox authoring and verification
- `L2` restricted gameplay-loop prototype
- cold compile validation
- successful `BuildCookRun`
- packaged Windows build launch verification

At the benchmark level, the current prototype has already demonstrated:

- enemy spawning
- auto-attacks and kill counting
- XP drops and XP pickup flow
- level-up triggers
- upgrade application
- HUD feedback
- restart-capable survival loop scaffolding

The important boundary is that this repository stores the workflow, benchmark tooling, reports, and sanitized artifacts. The Unreal sample project, gameplay prototype code, maps, packaged builds, and raw local logs stay outside this repo as external benchmark assets.

See the benchmark write-up and artifact boundary notes here:

- [`docs/unreal-ai-playbook/vampire-survivors-benchmark-pass.zh-CN.md`](./docs/unreal-ai-playbook/vampire-survivors-benchmark-pass.zh-CN.md)
- [`docs/unreal-ai-playbook/benchmark-artifact-guidelines.zh-CN.md`](./docs/unreal-ai-playbook/benchmark-artifact-guidelines.zh-CN.md)
## Features

- **Project setup** – Configure `.uproject` once; engine auto-detected from registry
- **Build & launch** – Compile via UBT, launch editor, wait for MCP readiness
- **Plugin install** – One-click RemoteMCP installation (local copy or GitHub download)
- **Instance discovery** — Scan ports to find running UE editors
- **UE tool proxy** — `ue_run_python`, `ue_call`, `ue_list_tools` and domain dispatch
- **Crash resilience** — Crash detection, report retrieval, restart flow
- **Multi-instance** — Switch between multiple UE editors via `use_editor`
- **Session notes** — Persist context for crash recovery
- **One-click overview** — `hub_status` shows project, plugin, instances, and watcher state

## Quick Install

### Option A: One-line install from PyPI (recommended)

```bash
# uv (recommended)
uv tool install unrealhub

# or pip
pip install unrealhub
```

Then add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "unrealhub": {
      "command": "unrealhub",
      "args": ["serve"]
    }
  }
}
```

### Option B: Zero-install (auto-fetch on first launch)

No download, no clone, no install. Paste this single block into `.cursor/mcp.json` and restart Cursor:

```json
{
  "mcpServers": {
    "unrealhub": {
      "command": "uvx",
      "args": ["unrealhub", "serve"]
    }
  }
}
```

> Requires [uv](https://docs.astral.sh/uv/getting-started/installation/) (`pip install uv` or `winget install astral-sh.uv`). Cursor will auto-fetch the Hub on first launch.

### Option C: Standalone executable (no Python needed)

Download the latest executable for your platform from [GitHub Releases](https://github.com/blackplume233/UnrealMCPHub/releases), then:

```json
{
  "mcpServers": {
    "unrealhub": {
      "command": "/path/to/unrealhub",
      "args": ["serve"]
    }
  }
}
```

| Platform | File |
|----------|------|
| Windows x64 | `unrealhub-windows-amd64.exe` |
| macOS ARM | `unrealhub-macos-arm64` |
| Linux x64 | `unrealhub-linux-amd64` |

### Option D: Clone for development

```bash
git clone https://github.com/blackplume233/UnrealMCPHub.git
cd UnrealMCPHub
uv sync          # or: pip install -e .
```

```json
{
  "mcpServers": {
    "unrealhub": {
      "command": "uv",
      "args": ["--directory", "/path/to/UnrealMCPHub", "run", "unrealhub", "serve"]
    }
  }
}
```

## Quick Start

### For AI Clients (Cursor / Claude / Codex app / Codex CLI / etc.)

This is the primary use case. Add UnrealMCPHub as an MCP server in any MCP-capable AI client, then let the agent handle the Unreal workflow through natural language.

That includes tools such as:

- Cursor
- Claude Desktop
- Codex app
- Codex CLI
- other MCP-compatible agent clients

**Step 1: Install & Configure MCP** (see [Quick Install](#quick-install-30-seconds) above)

**HTTP mode** (for shared / remote / multi-client use):

```bash
unrealhub serve --http --port <hub-port>
```

```json
{
  "mcpServers": {
    "unrealhub": {
      "url": "http://<hub-host>:<hub-port>/mcp"
    }
  }
}
```

**Step 2: Talk to the agent**

Once configured, the AI agent has full access to all Hub tools. Example conversations:

```
You: "帮我编译并启动 UE 项目 D:/Projects/MyGame/MyGame.uproject"
Agent: [calls setup_project, compile_project, launch_editor automatically]

You: "在 UE 里创建一个蓝图 Actor"
Agent: [calls ue_get_dispatch to find blueprint tools, then ue_call_dispatch]

You: "UE 崩溃了怎么办"
Agent: [calls get_crash_report, shows crash info, offers restart_editor]
```

**Step 3: What happens behind the scenes**

```
Agent → Hub (setup_project)     # One-time project config, persisted
Agent → Hub (compile_project)   # Compiles via UBT, even without UE running
Agent → Hub (launch_editor)     # Starts UE, waits for MCP readiness
Agent → Hub (ue_run_python)     # Hub forwards to UE's RemoteMCP
                ↓
        UE Editor (plugin MCP endpoint)   # Executes Python, returns result
```

The agent only needs to know about the Hub — it never talks to UE directly.

For Codex surfaces specifically:

- **Codex app** can connect to the Hub as a local MCP server and use the same natural-language workflow as other MCP-enabled desktop clients.
- **Codex CLI** can also work with this setup when its MCP configuration points at the same Hub server, which makes it useful for scripted or terminal-first Unreal workflows.

### AI Agent Decision Flow

```
Is project configured?
├── No  → Ask user for .uproject path → setup_project()
└── Yes → Is UE Editor online?
          ├── No  → Need plugin? → install_plugin() → compile_project() → launch_editor()
          └── Yes → Use ue_* tools directly
                    └── Crashed? → get_crash_report() → restart_editor()
```

### For Humans (CLI)

```bash
unrealhub setup /path/to/MyProject.uproject    # Configure project
unrealhub serve                                 # Start MCP server (stdio)
unrealhub serve --http --port <hub-port>        # Start MCP server (HTTP)
unrealhub status                                # Show instance status
unrealhub discover                              # Discover running UE instances
unrealhub compile                               # Build active project
unrealhub launch                                # Launch editor
```

## Tool Reference

### Hub Management (always available, even without UE)

| Tool | Description |
|------|-------------|
| `setup_project` | Configure project path (once, persisted to `~/.unrealhub`) |
| `get_project_config` | View current project configuration |
| `hub_status` | One-stop overview of everything |
| `compile_project` | Compile project via UBT |
| `launch_editor` | Start UE Editor, wait for MCP readiness |
| `restart_editor` | Restart a crashed editor |
| `install_plugin` | Install RemoteMCP plugin |
| `set_plugin_source` | Configure plugin download URL or local path |
| `discover_instances` | Scan ports for running UE instances |
| `use_editor` | Switch active UE instance (multi-instance) |
| `get_crash_report` | Get crash details |
| `add_note` / `get_notes` | Session notes for crash recovery context |

### UE Proxy Tools (forwarded to active UE instance)

| Tool | Description |
|------|-------------|
| `ue_run_python` | Execute Python script in UE |
| `ue_call` | Call any UE MCP tool by name |
| `ue_list_tools` | List all tools from UE instance |
| `ue_get_dispatch` | List domain tools (level, blueprint, umg, etc.) |
| `ue_call_dispatch` | Call a domain-specific tool |
| `ue_test_state` | Test connection to UE |
| `ue_status` | Get active instance status |

## Architecture

```
┌─────────────────┐     stdio/HTTP      ┌──────────────────┐
│  Cursor / Agent │ ◄─────────────────► │  UnrealMCPHub    │
└─────────────────┘                     │  (FastMCP Server) │
                                        └────────┬─────────┘
                                                 │
                 ┌───────────────────────────────┼───────────────────────────────┐
                 │                               │                               │
                 ▼                               ▼                               ▼
         ┌───────────────┐              ┌───────────────┐              ┌───────────────┐
         │ Project Mgmt  │              │ Lifecycle     │              │ UE Proxy      │
         │ setup_project │              │ compile       │              │ ue_run_python  │
         │ install_plugin│              │ launch/restart│              │ ue_call        │
         │ hub_status    │              │ discover      │              │ ue_list_tools  │
         └───────────────┘              └───────┬───────┘              └───────┬───────┘
                 │                              │                              │
                 ▼                              │  Streamable HTTP             │
         ┌───────────────┐              ┌──────▼──────────────────────────────▼────────┐
          │ ~/.unrealhub  │              │  UE Editor + RemoteMCP (runtime endpoint)      │
         │ config.json   │              │  17+ tools: run_python, get_dispatch, etc.    │
         │ state.json    │              │  6 domains: level, blueprint, umg, edgraph,   │
         └───────────────┘              │             behaviortree, slate               │
                                        └──────────────────────────────────────────────┘
```

## Development

```bash
git clone https://github.com/blackplume233/UnrealMCPHub.git
cd UnrealMCPHub
uv sync --extra dev      # Install with dev dependencies
uv run pytest tests/ -v  # Run tests (129 tests)
```

## Requirements

- Python >= 3.11
- Unreal Engine 5.x
- [RemoteMCP](https://github.com/blackplume233/UnrealRemoteMCP) — UE Editor plugin (Hub can auto-install it via `install_plugin`)

## License

MIT
