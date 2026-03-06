# UnrealMCPHub

Central management platform for Unreal Engine MCP instances—bridge between AI agents and UE across the full development lifecycle.

## Features

- **Project setup** — Configure `.uproject` once; engine auto-detected from registry
- **Build & launch** — Compile via UBT, launch editor, wait for MCP readiness
- **Instance discovery** — Scan ports to find running UE editors
- **UE tool proxy** — `ue_run_python`, `ue_call`, `ue_list_tools` and domain dispatch
- **Crash resilience** — Crash detection, report retrieval, restart flow
- **Multi-instance** — Switch between multiple UE editors via `use_editor`
- **Session notes** — Persist context for crash recovery

## Installation

```bash
# pip
pip install -e .

# uv
uv pip install -e .
```

## Quick Start

### MCP configuration (Cursor)

Add to `.cursor/mcp.json` or Cursor MCP settings:

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

Or with uv:

```json
{
  "mcpServers": {
    "unrealhub": {
      "command": "uv",
      "args": ["run", "unrealhub", "serve"]
    }
  }
}
```

### CLI usage

```bash
unrealhub setup /path/to/MyProject.uproject   # Configure project
unrealhub serve                               # Start MCP server (stdio)
unrealhub serve --http --port 9422             # Start MCP server (HTTP)
unrealhub status                              # Show instance status
unrealhub discover                            # Discover running UE instances
unrealhub compile                             # Build active project
unrealhub launch                              # Launch editor
```

## Architecture

```
┌─────────────────┐     stdio/HTTP      ┌──────────────────┐
│  Cursor / Agent │ ◄─────────────────► │  UnrealMCPHub    │
└─────────────────┘                    │  (MCP Server)     │
                                       └────────┬─────────┘
                                                │
                    ┌────────────────────────────┼────────────────────────────┐
                    │                            │                            │
                    ▼                            ▼                            ▼
            ┌───────────────┐           ┌───────────────┐           ┌───────────────┐
            │ setup_project │           │ launch_editor │           │ ue_run_python  │
            │ compile       │           │ discover      │           │ ue_call        │
            │ install_plugin│           │ restart       │           │ ue_list_tools  │
            └───────────────┘           └───────┬───────┘           └───────┬───────┘
                    │                           │                           │
                    │                           │  HTTP/MCP                 │
                    ▼                           ▼                           ▼
            ┌───────────────┐           ┌───────────────────────────────────────┐
            │ ~/.unrealhub  │           │  UE Editor + RemoteMCP (port 8422)    │
            │ config.json   │           │  - run_python_script                   │
            └───────────────┘           │  - get_dispatch / call_dispatch       │
                                        └───────────────────────────────────────┘
```

## License

MIT
