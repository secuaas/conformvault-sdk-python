"""Tests for the ConformVault Python SDK client and service layers."""

from __future__ import annotations

import json
from typing import Any, Dict

import httpx
import pytest

import conformvault
from conformvault import (
    APIError,
    AsyncConformVault,
    AuthenticationError,
    ConformVault,
    CreateAPIKeyRequest,
    CreateFolderRequest,
    CreateShareLinkRequest,
    CreateSignatureRequest,
    CreateSignatureSigner,
    RateLimitError,
    RegisterWebhookRequest,
    is_not_found,
    is_rate_limited,
)
from conformvault.client import USER_AGENT


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _json_response(data: Any, status_code: int = 200) -> httpx.Response:
    """Build a fake httpx.Response with JSON content."""
    content = json.dumps(data).encode()
    return httpx.Response(
        status_code=status_code,
        content=content,
        headers={"content-type": "application/json"},
    )


def _mock_transport(handler):
    """Create an httpx.MockTransport from a simple handler function."""
    return httpx.MockTransport(handler)


# ---------------------------------------------------------------------------
# Client instantiation
# ---------------------------------------------------------------------------

class TestClientInit:

    def test_defaults(self):
        client = ConformVault("test-key")
        assert client._http._base_url == conformvault.DEFAULT_BASE_URL
        assert client._http._api_key == "test-key"
        assert client.files is not None
        assert client.folders is not None
        assert client.share_links is not None
        assert client.signatures is not None
        assert client.webhooks is not None
        assert client.audit is not None
        assert client.keys is not None

    def test_custom_base_url(self):
        client = ConformVault("key", base_url="https://custom.example.com/api")
        assert client._http._base_url == "https://custom.example.com/api"

    def test_context_manager(self):
        with ConformVault("key") as client:
            assert client.files is not None


# ---------------------------------------------------------------------------
# Files service
# ---------------------------------------------------------------------------

class TestFilesService:

    def test_list_files(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/files"
            assert request.headers["authorization"] == "Bearer test-key"
            assert request.headers["user-agent"] == USER_AGENT
            return _json_response({
                "data": [
                    {"id": "f1", "name": "test.pdf", "original_name": "test.pdf", "size": 1024},
                    {"id": "f2", "name": "doc.txt", "original_name": "doc.txt", "size": 512},
                ]
            })

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("test-key", base_url="https://api.test.com", http_client=http_client)

        files = client.files.list()
        assert len(files) == 2
        assert files[0].id == "f1"
        assert files[0].name == "test.pdf"
        assert files[0].size == 1024
        assert files[1].id == "f2"

    def test_list_files_with_params(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert "folder_id=fold1" in str(request.url)
            assert "page=2" in str(request.url)
            assert "limit=10" in str(request.url)
            return _json_response({"data": []})

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        files = client.files.list(folder_id="fold1", page=2, limit=10)
        assert files == []

    def test_get_file(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/files/f1"
            return _json_response({
                "data": {"id": "f1", "name": "test.pdf", "original_name": "test.pdf", "size": 2048, "content_type": "application/pdf"}
            })

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        f = client.files.get("f1")
        assert f.id == "f1"
        assert f.content_type == "application/pdf"

    def test_upload_file(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "POST"
            assert request.url.path == "/files"
            assert b"file" in request.content or b"multipart" in request.headers.get("content-type", "").encode()
            return _json_response({
                "data": {"id": "f-new", "name": "upload.txt", "original_name": "upload.txt", "size": 11}
            })

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        result = client.files.upload(b"hello world", "upload.txt")
        assert result.id == "f-new"
        assert result.size == 11

    def test_delete_file(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "DELETE"
            assert request.url.path == "/files/f1"
            return httpx.Response(204)

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        client.files.delete("f1")  # should not raise


# ---------------------------------------------------------------------------
# Folders service
# ---------------------------------------------------------------------------

class TestFoldersService:

    def test_list_folders(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return _json_response({
                "data": [
                    {"id": "d1", "name": "Documents", "path": "/Documents"},
                ]
            })

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        folders = client.folders.list()
        assert len(folders) == 1
        assert folders[0].name == "Documents"

    def test_create_folder(self):
        def handler(request: httpx.Request) -> httpx.Response:
            body = json.loads(request.content)
            assert body["name"] == "New Folder"
            return _json_response({
                "data": {"id": "d2", "name": "New Folder", "path": "/New Folder"}
            }, status_code=201)

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        folder = client.folders.create(CreateFolderRequest(name="New Folder"))
        assert folder.id == "d2"
        assert folder.name == "New Folder"

    def test_get_folder(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/folders/d1"
            return _json_response({
                "data": {"id": "d1", "name": "Docs", "path": "/Docs"}
            })

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        folder = client.folders.get("d1")
        assert folder.id == "d1"

    def test_delete_folder(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "DELETE"
            return httpx.Response(204)

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        client.folders.delete("d1")


# ---------------------------------------------------------------------------
# ShareLinks service
# ---------------------------------------------------------------------------

class TestShareLinksService:

    def test_list_share_links(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return _json_response({
                "data": [
                    {"id": "sl1", "token": "abc", "url": "https://...", "type": "download", "is_active": True},
                ]
            })

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        links = client.share_links.list()
        assert len(links) == 1
        assert links[0].type == "download"

    def test_create_share_link(self):
        def handler(request: httpx.Request) -> httpx.Response:
            body = json.loads(request.content)
            assert body["type"] == "download"
            return _json_response({
                "data": {"id": "sl2", "token": "xyz", "url": "https://share/xyz", "type": "download", "is_active": True}
            }, status_code=201)

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        link = client.share_links.create(CreateShareLinkRequest(file_id="f1", type="download"))
        assert link.token == "xyz"

    def test_delete_share_link(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "DELETE"
            return httpx.Response(204)

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        client.share_links.delete("sl1")


# ---------------------------------------------------------------------------
# Signatures service
# ---------------------------------------------------------------------------

class TestSignaturesService:

    def test_create_signature(self):
        def handler(request: httpx.Request) -> httpx.Response:
            body = json.loads(request.content)
            assert body["subject"] == "NDA Agreement"
            assert len(body["signers"]) == 1
            return _json_response({
                "data": {
                    "id": "env-123",
                    "provider": "boldsign",
                    "status": "sent",
                    "subject": "NDA Agreement",
                    "expiry_days": 30,
                }
            }, status_code=201)

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        env = client.signatures.create(CreateSignatureRequest(
            file_id="file-abc",
            subject="NDA Agreement",
            signers=[CreateSignatureSigner(email="signer@example.com", name="John Doe")],
            expiry_days=30,
        ))
        assert env.id == "env-123"
        assert env.status == "sent"

    def test_get_status(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/signatures/env-123"
            return _json_response({
                "data": {"id": "env-123", "status": "completed", "subject": "NDA"}
            })

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        env = client.signatures.get_status("env-123")
        assert env.status == "completed"

    def test_revoke(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "POST"
            assert request.url.path == "/signatures/env-123/revoke"
            return httpx.Response(204)

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        client.signatures.revoke("env-123")


# ---------------------------------------------------------------------------
# Webhooks service
# ---------------------------------------------------------------------------

class TestWebhooksService:

    def test_list_webhooks(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return _json_response({
                "data": [
                    {"id": "wh1", "url": "https://hook.example.com", "events": ["file.uploaded"], "is_active": True},
                ]
            })

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        hooks = client.webhooks.list()
        assert len(hooks) == 1
        assert hooks[0].events == ["file.uploaded"]

    def test_register_webhook(self):
        def handler(request: httpx.Request) -> httpx.Response:
            body = json.loads(request.content)
            assert body["url"] == "https://hook.example.com"
            return _json_response({
                "data": {
                    "id": "wh2",
                    "url": "https://hook.example.com",
                    "events": ["*"],
                    "is_active": True,
                    "secret": "whsec_abc123",
                }
            }, status_code=201)

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        resp = client.webhooks.register(RegisterWebhookRequest(url="https://hook.example.com"))
        assert resp.secret == "whsec_abc123"

    def test_delete_webhook(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "DELETE"
            return httpx.Response(204)

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        client.webhooks.delete("wh1")

    def test_test_webhook(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "POST"
            assert request.url.path == "/webhooks/wh1/test"
            return httpx.Response(204)

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        client.webhooks.test("wh1")


# ---------------------------------------------------------------------------
# Audit service
# ---------------------------------------------------------------------------

class TestAuditService:

    def test_list_audit(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return _json_response({
                "data": [
                    {"id": "a1", "action": "file.uploaded", "resource_type": "file", "resource_id": "f1"},
                ]
            })

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        entries = client.audit.list()
        assert len(entries) == 1
        assert entries[0].action == "file.uploaded"

    def test_list_audit_with_filters(self):
        def handler(request: httpx.Request) -> httpx.Response:
            url_str = str(request.url)
            assert "event_type=file.deleted" in url_str
            assert "from=2025-01-01" in url_str
            assert "to=2025-12-31" in url_str
            assert "page=1" in url_str
            assert "limit=50" in url_str
            return _json_response({"data": []})

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        entries = client.audit.list(
            event_type="file.deleted",
            from_date="2025-01-01",
            to_date="2025-12-31",
            page=1,
            limit=50,
        )
        assert entries == []


# ---------------------------------------------------------------------------
# Keys service
# ---------------------------------------------------------------------------

class TestKeysService:

    def test_list_keys(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return _json_response({
                "data": [
                    {"id": "k1", "name": "Prod Key", "prefix": "cvk_live_", "environment": "live", "scopes": ["files:read"]},
                ]
            })

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        keys = client.keys.list()
        assert len(keys) == 1
        assert keys[0].name == "Prod Key"

    def test_create_key(self):
        def handler(request: httpx.Request) -> httpx.Response:
            body = json.loads(request.content)
            assert body["name"] == "Test Key"
            return _json_response({
                "data": {
                    "id": "k2",
                    "name": "Test Key",
                    "prefix": "cvk_test_",
                    "environment": "test",
                    "scopes": ["*"],
                    "key": "cvk_test_full_secret_key",
                }
            }, status_code=201)

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        resp = client.keys.create(CreateAPIKeyRequest(name="Test Key", environment="test", scopes=["*"]))
        assert resp.key == "cvk_test_full_secret_key"

    def test_get_key(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/keys/k1"
            return _json_response({
                "data": {"id": "k1", "name": "My Key", "prefix": "cvk_live_", "environment": "live", "scopes": ["files:read"]}
            })

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        key = client.keys.get("k1")
        assert key.id == "k1"

    def test_revoke_key(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "DELETE"
            return httpx.Response(204)

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        client.keys.revoke("k1")

    def test_rotate_key(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "POST"
            assert request.url.path == "/keys/k1/rotate"
            return _json_response({
                "data": {
                    "id": "k1",
                    "name": "Rotated",
                    "prefix": "cvk_live_",
                    "environment": "live",
                    "scopes": ["*"],
                    "key": "cvk_live_new_rotated_key",
                }
            })

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        resp = client.keys.rotate("k1")
        assert resp.key == "cvk_live_new_rotated_key"


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

class TestErrorHandling:

    def test_rate_limit_error(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                429,
                json={"error": "rate limited"},
                headers={"Retry-After": "30"},
            )

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        with pytest.raises(RateLimitError) as exc_info:
            client.files.list()
        assert exc_info.value.retry_after == 30.0
        assert is_rate_limited(exc_info.value)

    def test_not_found_error(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(404, json={"error": "file not found"})

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        with pytest.raises(APIError) as exc_info:
            client.files.get("nonexistent")
        assert exc_info.value.status_code == 404
        assert is_not_found(exc_info.value)

    def test_authentication_error(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(401, json={"error": "invalid api key"})

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("bad-key", base_url="https://api.test.com", http_client=http_client)

        with pytest.raises(AuthenticationError) as exc_info:
            client.files.list()
        assert exc_info.value.status_code == 401

    def test_generic_api_error(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(500, json={"error": "internal server error"})

        transport = _mock_transport(handler)
        http_client = httpx.Client(transport=transport)
        client = ConformVault("key", base_url="https://api.test.com", http_client=http_client)

        with pytest.raises(APIError) as exc_info:
            client.files.list()
        assert exc_info.value.status_code == 500
        assert "internal server error" in str(exc_info.value)


# ---------------------------------------------------------------------------
# Async client
# ---------------------------------------------------------------------------

class TestAsyncClient:

    @pytest.mark.anyio
    async def test_async_list_files(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            assert request.headers["authorization"] == "Bearer async-key"
            return _json_response({
                "data": [
                    {"id": "af1", "name": "async.pdf", "original_name": "async.pdf", "size": 256},
                ]
            })

        transport = httpx.MockTransport(handler)
        http_client = httpx.AsyncClient(transport=transport)
        async with AsyncConformVault("async-key", base_url="https://api.test.com", http_client=http_client) as client:
            files = await client.files.list()
            assert len(files) == 1
            assert files[0].id == "af1"

    @pytest.mark.anyio
    async def test_async_create_folder(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            body = json.loads(request.content)
            assert body["name"] == "Async Folder"
            return _json_response({
                "data": {"id": "ad1", "name": "Async Folder", "path": "/Async Folder"}
            }, status_code=201)

        transport = httpx.MockTransport(handler)
        http_client = httpx.AsyncClient(transport=transport)
        async with AsyncConformVault("key", base_url="https://api.test.com", http_client=http_client) as client:
            folder = await client.folders.create(CreateFolderRequest(name="Async Folder"))
            assert folder.id == "ad1"

    @pytest.mark.anyio
    async def test_async_error_handling(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(429, json={"error": "slow down"}, headers={"Retry-After": "15"})

        transport = httpx.MockTransport(handler)
        http_client = httpx.AsyncClient(transport=transport)
        async with AsyncConformVault("key", base_url="https://api.test.com", http_client=http_client) as client:
            with pytest.raises(RateLimitError) as exc_info:
                await client.files.list()
            assert exc_info.value.retry_after == 15.0
