"""UnrealMCPHub - Central management platform for Unreal Engine MCP instances."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("unrealhub")
except PackageNotFoundError:
    # Fallback for running directly from a source checkout without installed metadata.
    __version__ = "0.3.1"
