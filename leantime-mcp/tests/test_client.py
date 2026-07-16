# SPDX-License-Identifier: MIT

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from leantime_mcp.client import LeantimeClient


def _mock_http_client() -> MagicMock:
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json.return_value = {"result": True}

    client = AsyncMock()
    client.post = AsyncMock(return_value=response)

    context = MagicMock()
    context.__aenter__ = AsyncMock(return_value=client)
    context.__aexit__ = AsyncMock(return_value=None)
    return context


@pytest.fixture
def client() -> LeantimeClient:
    return LeantimeClient("https://leantime.example.com", "pat-token-abc")


@pytest.mark.asyncio
async def test_call_uses_bearer_header(client: LeantimeClient):
    with patch("httpx.AsyncClient", return_value=_mock_http_client()) as client_cls:
        await client.call("leantime.rpc.Projects.getAll")

        assert client_cls.call_args.kwargs["verify"] is True
        post = client_cls.return_value.__aenter__.return_value.post
        headers = post.await_args.kwargs["headers"]
        assert headers["Authorization"] == "Bearer pat-token-abc"
        assert "X-API-KEY" not in headers


@pytest.mark.asyncio
async def test_call_can_disable_ssl_verify():
    client = LeantimeClient("https://leantime.example.com", "pat", verify_ssl=False)
    with patch("httpx.AsyncClient", return_value=_mock_http_client()) as client_cls:
        await client.call("leantime.rpc.Projects.getAll")

        assert client_cls.call_args.kwargs["verify"] is False


@pytest.mark.asyncio
async def test_add_comment_uses_comments_rpc(client: LeantimeClient):
    client.get_ticket = AsyncMock(return_value={"projectId": 42})

    with patch.object(client, "call", new_callable=AsyncMock) as call:
        call.return_value = True

        await client.add_comment("ticket", 99, "hello")

        method, params = call.await_args.args
        assert method == "leantime.rpc.Comments.Comments.addComment"
        assert params["values"]["text"] == "hello"
        assert params["values"]["ticketId"] == 99
        assert params["values"]["projectId"] == 42
        assert "userId" not in params["values"]


@pytest.mark.asyncio
async def test_edit_comment_uses_comments_rpc(client: LeantimeClient):
    with patch.object(client, "call", new_callable=AsyncMock) as call:
        call.return_value = True

        await client.edit_comment(55, "updated text")

        method, params = call.await_args.args
        assert method == "leantime.rpc.Comments.Comments.editComment"
        assert params == {"id": 55, "values": {"text": "updated text"}}


@pytest.mark.asyncio
async def test_delete_comment_uses_comments_rpc(client: LeantimeClient):
    with patch.object(client, "call", new_callable=AsyncMock) as call:
        call.return_value = True

        await client.delete_comment(55)

        method, params = call.await_args.args
        assert method == "leantime.rpc.Comments.Comments.deleteComment"
        assert params == {"commentId": 55}


@pytest.mark.asyncio
async def test_update_ticket_uses_patch_not_full_update(client: LeantimeClient):
    """updateTicket wipes omitted fields; patchTicket is partial-safe."""
    with patch.object(client, "call", new_callable=AsyncMock) as call:
        call.return_value = True

        await client.update_ticket(283, 21, status=2, assignedTo=4)

        method, params = call.await_args.args
        assert method == "leantime.rpc.Tickets.Tickets.patchTicket"
        assert params == {"id": 283, "values": {"status": 2, "editorId": 4}}
        assert "description" not in params["values"]
        assert "assignedTo" not in params["values"]


@pytest.mark.asyncio
async def test_update_ticket_maps_description_headline_priority(client: LeantimeClient):
    with patch.object(client, "call", new_callable=AsyncMock) as call:
        call.return_value = True

        await client.update_ticket(
            10, 1, headline="h", description="<p>d</p>", priority="3"
        )

        method, params = call.await_args.args
        assert method == "leantime.rpc.Tickets.Tickets.patchTicket"
        assert params["values"] == {
            "headline": "h",
            "description": "<p>d</p>",
            "priority": "3",
        }
