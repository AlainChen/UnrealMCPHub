import asyncio
import base64
import logging
from datetime import timedelta
from typing import Any

import httpx

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.shared._httpx_utils import create_mcp_http_client

logger = logging.getLogger(__name__)


def _serialize_content_item(item: Any) -> dict[str, Any]:
    type_name = type(item).__name__
    if type_name == "TextContent":
        return {"type": "text", "text": getattr(item, "text", str(item))}
    if type_name == "ImageContent":
        data = getattr(item, "data", b"")
        if isinstance(data, bytes):
            data = base64.b64encode(data).decode("ascii")
        return {
            "type": "image",
            "data": data,
            "mimeType": getattr(item, "mimeType", "application/octet-stream"),
        }
    return {"type": type_name, "repr": repr(item)}


class UEMCPClient:
    """MCP client for a remote UE instance.

    Uses per-call connections to avoid cancel-scope conflicts when called
    from within FastMCP tool handlers (anyio task groups).
    """

    def __init__(
        self,
        url: str,
        timeout_connect: float = 5.0,
        timeout_read: float = 300.0,
    ):
        self.url = url
        self.timeout_connect = timeout_connect
        self.timeout_read = timeout_read
        self._reachable: bool | None = None

    @property
    def connected(self) -> bool:
        return self._reachable is True

    async def _open_session(self):
        """Context manager that yields a ready ClientSession."""

        class _Ctx:
            def __init__(self, url, tc, tr):
                self._url = url
                self._tc = tc
                self._tr = tr
                self._http = None
                self._transport_ctx = None
                self._session = None
                self._r = None
                self._w = None

            async def __aenter__(self):
                self._http = create_mcp_http_client(
                    timeout=httpx.Timeout(self._tr, connect=self._tc)
                )
                await self._http.__aenter__()
                self._transport_ctx = streamable_http_client(
                    self._url,
                    http_client=self._http,
                    terminate_on_close=False,
                )
                self._r, self._w, _ = await self._transport_ctx.__aenter__()
                self._session = ClientSession(
                    self._r,
                    self._w,
                    read_timeout_seconds=timedelta(seconds=self._tr),
                )
                s = await self._session.__aenter__()
                await s.initialize()
                return s

            async def __aexit__(self, *exc):
                errors = []
                for ctx in (self._session, self._transport_ctx, self._http):
                    if ctx is not None:
                        try:
                            await ctx.__aexit__(*exc)
                        except Exception as e:
                            errors.append(e)
                if errors:
                    logger.debug("Cleanup errors (non-fatal): %s", errors)
                return False

        return _Ctx(self.url, self.timeout_connect, self.timeout_read)

    async def call_tool(
        self,
        name: str,
        arguments: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            async with await self._open_session() as session:
                result = await session.call_tool(
                    name,
                    arguments or {},
                    read_timeout_seconds=timedelta(seconds=self.timeout_read),
                )
                self._reachable = True
                content = [_serialize_content_item(item) for item in result.content]
                if result.isError:
                    error_msg = ""
                    for item in result.content:
                        if hasattr(item, "text"):
                            error_msg += getattr(item, "text", "")
                    return {"success": False, "content": content, "error": error_msg or "Tool returned error"}
                return {"success": True, "content": content, "error": None}
        except Exception as exc:
            logger.exception("call_tool %s failed: %s", name, exc)
            self._reachable = False
            return {"success": False, "content": [], "error": str(exc)}

    async def list_tools(self) -> list[dict[str, Any]]:
        try:
            async with await self._open_session() as session:
                result = await session.list_tools()
                self._reachable = True
                return [
                    {
                        "name": t.name,
                        "description": getattr(t, "description", "") or "",
                        "inputSchema": getattr(t, "inputSchema", None) or {},
                    }
                    for t in result.tools
                ]
        except Exception as exc:
            logger.exception("list_tools failed: %s", exc)
            self._reachable = False
            return []

    async def health_check(self) -> bool:
        try:
            async with await self._open_session() as session:
                await asyncio.wait_for(session.list_tools(), timeout=5.0)
                self._reachable = True
                return True
        except Exception:
            self._reachable = False
            return False

    @staticmethod
    async def probe_endpoint(url: str, timeout: float = 3.0) -> bool:
        """Quick HTTP probe without establishing a full MCP session."""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(timeout)) as client:
                resp = await client.post(
                    url,
                    json={
                        "jsonrpc": "2.0",
                        "method": "initialize",
                        "id": 1,
                        "params": {
                            "protocolVersion": "2025-03-26",
                            "capabilities": {},
                            "clientInfo": {"name": "unrealhub-probe", "version": "0.1.0"},
                        },
                    },
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json, text/event-stream",
                    },
                )
                return resp.status_code in (200, 201, 202)
        except Exception:
            return False
