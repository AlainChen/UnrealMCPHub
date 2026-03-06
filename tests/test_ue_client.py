import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from unrealhub.ue_client import UEMCPClient, _serialize_content_item


class TestSerializeContentItem:
    def test_text_content(self):
        item = MagicMock()
        type(item).__name__ = "TextContent"
        item.text = "hello"
        result = _serialize_content_item(item)
        assert result == {"type": "text", "text": "hello"}

    def test_text_content_fallback(self):
        item = MagicMock()
        type(item).__name__ = "TextContent"
        del item.text
        result = _serialize_content_item(item)
        assert result["type"] == "text"

    def test_image_content_bytes(self):
        item = MagicMock()
        type(item).__name__ = "ImageContent"
        item.data = b"\x89PNG"
        item.mimeType = "image/png"
        result = _serialize_content_item(item)
        assert result["type"] == "image"
        assert result["mimeType"] == "image/png"
        assert isinstance(result["data"], str)

    def test_image_content_str(self):
        item = MagicMock()
        type(item).__name__ = "ImageContent"
        item.data = "already_base64"
        item.mimeType = "image/jpeg"
        result = _serialize_content_item(item)
        assert result["data"] == "already_base64"

    def test_unknown_content_type(self):
        item = MagicMock()
        type(item).__name__ = "EmbeddedResource"
        result = _serialize_content_item(item)
        assert result["type"] == "EmbeddedResource"
        assert "repr" in result


class TestUEMCPClient:
    def test_init(self):
        client = UEMCPClient("http://localhost:8422/mcp")
        assert client.url == "http://localhost:8422/mcp"
        assert client.timeout_connect == 5.0
        assert client.timeout_read == 300.0
        assert not client.connected

    def test_connected_property(self):
        client = UEMCPClient("http://localhost:8422/mcp")
        assert not client.connected
        client._reachable = True
        assert client.connected
        client._reachable = False
        assert not client.connected
        client._reachable = None
        assert not client.connected

    @pytest.mark.asyncio
    async def test_call_tool_connection_failure(self):
        client = UEMCPClient("http://localhost:99999/mcp", timeout_connect=0.1)

        async def _broken_session():
            raise ConnectionError("refused")

        with patch.object(client, "_open_session", side_effect=_broken_session):
            result = await client.call_tool("test_tool", {})
        assert not result["success"]
        assert result["content"] == []
        assert result["error"]
        assert not client.connected

    @pytest.mark.asyncio
    async def test_list_tools_connection_failure(self):
        client = UEMCPClient("http://localhost:99999/mcp", timeout_connect=0.1)

        async def _broken_session():
            raise ConnectionError("refused")

        with patch.object(client, "_open_session", side_effect=_broken_session):
            tools = await client.list_tools()
        assert tools == []
        assert not client.connected

    @pytest.mark.asyncio
    async def test_health_check_failure(self):
        client = UEMCPClient("http://localhost:99999/mcp", timeout_connect=0.1)

        async def _broken_session():
            raise ConnectionError("refused")

        with patch.object(client, "_open_session", side_effect=_broken_session):
            result = await client.health_check()
        assert result is False
        assert not client.connected

    @pytest.mark.asyncio
    async def test_probe_endpoint_no_server(self):
        result = await UEMCPClient.probe_endpoint(
            "http://localhost:99999/mcp", timeout=0.5
        )
        assert result is False

    @pytest.mark.asyncio
    async def test_probe_endpoint_success(self):
        import httpx

        async def mock_post(*args, **kwargs):
            resp = MagicMock()
            resp.status_code = 200
            return resp

        with patch("httpx.AsyncClient") as MockClient:
            ctx = AsyncMock()
            ctx.__aenter__ = AsyncMock(return_value=ctx)
            ctx.__aexit__ = AsyncMock(return_value=False)
            ctx.post = mock_post
            MockClient.return_value = ctx

            result = await UEMCPClient.probe_endpoint("http://localhost:8422/mcp")
            assert result is True

    @pytest.mark.asyncio
    async def test_probe_endpoint_non_200(self):
        async def mock_post(*args, **kwargs):
            resp = MagicMock()
            resp.status_code = 404
            return resp

        with patch("httpx.AsyncClient") as MockClient:
            ctx = AsyncMock()
            ctx.__aenter__ = AsyncMock(return_value=ctx)
            ctx.__aexit__ = AsyncMock(return_value=False)
            ctx.post = mock_post
            MockClient.return_value = ctx

            result = await UEMCPClient.probe_endpoint("http://localhost:8422/mcp")
            assert result is False
