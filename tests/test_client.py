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
    CreateActivitySubscriptionRequest,
    CreateCommentRequest,
    CreateFolderRequest,
    CreateJobRequest,
    CreateShareLinkRequest,
    CreateSignatureRequest,
    CreateSignatureSigner,
    RateLimitError,
    RegisterWebhookRequest,
    UpdateCommentRequest,
    is_not_found,
    is_rate_limited,
)
from conformvault.client import DEFAULT_BASE_URL, USER_AGENT, _build_headers, _serialize_body


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


def _make_client(handler, api_key: str = "test-key") -> ConformVault:
    """Build a ConformVault client backed by a mock transport handler."""
    transport = _mock_transport(handler)
    http_client = httpx.Client(transport=transport)
    return ConformVault(api_key, base_url="https://api.test.com", http_client=http_client)


def _make_async_client(handler, api_key: str = "test-key") -> AsyncConformVault:
    """Build an AsyncConformVault client backed by a mock transport handler."""
    transport = httpx.MockTransport(handler)
    http_client = httpx.AsyncClient(transport=transport)
    return AsyncConformVault(api_key, base_url="https://api.test.com", http_client=http_client)


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

    def test_trailing_slash_stripped(self):
        client = ConformVault("key", base_url="https://api.example.com/v1/")
        assert client._http._base_url == "https://api.example.com/v1"

    def test_context_manager(self):
        with ConformVault("key") as client:
            assert client.files is not None

    def test_all_29_services_registered(self):
        """Every service should be set as an attribute on the client."""
        client = ConformVault("key")
        expected_services = [
            "files", "folders", "share_links", "signatures", "webhooks",
            "audit", "keys", "bulk", "versions", "search", "trash",
            "scan_reports", "attestation", "transactions", "templates",
            "batches", "metadata", "retention", "legal_holds", "permissions",
            "comments", "quota", "rate_limit", "upload_sessions", "jobs",
            "activity_subscriptions", "policies", "bandwidth", "data_export",
        ]
        for svc in expected_services:
            assert hasattr(client, svc), f"Missing service: {svc}"
            assert getattr(client, svc) is not None, f"Service is None: {svc}"
        assert len(expected_services) == 29

    def test_async_all_29_services_registered(self):
        """AsyncConformVault should also have all 29 services."""
        client = AsyncConformVault("key")
        expected_services = [
            "files", "folders", "share_links", "signatures", "webhooks",
            "audit", "keys", "bulk", "versions", "search", "trash",
            "scan_reports", "attestation", "transactions", "templates",
            "batches", "metadata", "retention", "legal_holds", "permissions",
            "comments", "quota", "rate_limit", "upload_sessions", "jobs",
            "activity_subscriptions", "policies", "bandwidth", "data_export",
        ]
        for svc in expected_services:
            assert hasattr(client, svc), f"Missing async service: {svc}"
            assert getattr(client, svc) is not None, f"Async service is None: {svc}"

    def test_build_headers(self):
        headers = _build_headers("my-api-key")
        assert headers["Authorization"] == "Bearer my-api-key"
        assert headers["User-Agent"] == USER_AGENT

    def test_serialize_body_none(self):
        assert _serialize_body(None) is None

    def test_serialize_body_dict_drops_none(self):
        result = _serialize_body({"a": 1, "b": None, "c": "hello"})
        assert result == {"a": 1, "c": "hello"}

    def test_serialize_body_dataclass(self):
        req = CreateFolderRequest(name="Test", parent_id=None)
        result = _serialize_body(req)
        assert result == {"name": "Test"}
        assert "parent_id" not in result


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

        client = _make_client(handler)
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

        client = _make_client(handler)
        files = client.files.list(folder_id="fold1", page=2, limit=10)
        assert files == []

    def test_get_file(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/files/f1"
            return _json_response({
                "data": {"id": "f1", "name": "test.pdf", "original_name": "test.pdf", "size": 2048, "content_type": "application/pdf"}
            })

        client = _make_client(handler)
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

        client = _make_client(handler)
        result = client.files.upload(b"hello world", "upload.txt")
        assert result.id == "f-new"
        assert result.size == 11

    def test_delete_file(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "DELETE"
            assert request.url.path == "/files/f1"
            return httpx.Response(204)

        client = _make_client(handler)
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

        client = _make_client(handler)
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

        client = _make_client(handler)
        folder = client.folders.create(CreateFolderRequest(name="New Folder"))
        assert folder.id == "d2"
        assert folder.name == "New Folder"

    def test_get_folder(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/folders/d1"
            return _json_response({
                "data": {"id": "d1", "name": "Docs", "path": "/Docs"}
            })

        client = _make_client(handler)
        folder = client.folders.get("d1")
        assert folder.id == "d1"

    def test_delete_folder(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "DELETE"
            return httpx.Response(204)

        client = _make_client(handler)
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

        client = _make_client(handler)
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

        client = _make_client(handler)
        link = client.share_links.create(CreateShareLinkRequest(file_id="f1", type="download"))
        assert link.token == "xyz"

    def test_delete_share_link(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "DELETE"
            return httpx.Response(204)

        client = _make_client(handler)
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

        client = _make_client(handler)
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

        client = _make_client(handler)
        env = client.signatures.get_status("env-123")
        assert env.status == "completed"

    def test_revoke(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "POST"
            assert request.url.path == "/signatures/env-123/revoke"
            return httpx.Response(204)

        client = _make_client(handler)
        client.signatures.revoke("env-123")

    def test_list_signatures(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/signatures"
            return _json_response({
                "data": [
                    {"id": "env-1", "status": "sent", "subject": "Doc A"},
                    {"id": "env-2", "status": "completed", "subject": "Doc B"},
                ]
            })

        client = _make_client(handler)
        envelopes = client.signatures.list()
        assert len(envelopes) == 2
        assert envelopes[0].id == "env-1"
        assert envelopes[1].status == "completed"


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

        client = _make_client(handler)
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

        client = _make_client(handler)
        resp = client.webhooks.register(RegisterWebhookRequest(url="https://hook.example.com"))
        assert resp.secret == "whsec_abc123"

    def test_delete_webhook(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "DELETE"
            return httpx.Response(204)

        client = _make_client(handler)
        client.webhooks.delete("wh1")

    def test_test_webhook(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "POST"
            assert request.url.path == "/webhooks/wh1/test"
            return httpx.Response(204)

        client = _make_client(handler)
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

        client = _make_client(handler)
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

        client = _make_client(handler)
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

        client = _make_client(handler)
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

        client = _make_client(handler)
        resp = client.keys.create(CreateAPIKeyRequest(name="Test Key", environment="test", scopes=["*"]))
        assert resp.key == "cvk_test_full_secret_key"

    def test_get_key(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/keys/k1"
            return _json_response({
                "data": {"id": "k1", "name": "My Key", "prefix": "cvk_live_", "environment": "live", "scopes": ["files:read"]}
            })

        client = _make_client(handler)
        key = client.keys.get("k1")
        assert key.id == "k1"

    def test_revoke_key(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "DELETE"
            return httpx.Response(204)

        client = _make_client(handler)
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

        client = _make_client(handler)
        resp = client.keys.rotate("k1")
        assert resp.key == "cvk_live_new_rotated_key"

    def test_instant_revoke(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "POST"
            assert request.url.path == "/api-keys/k1/revoke"
            return httpx.Response(204)

        client = _make_client(handler)
        client.keys.instant_revoke("k1")  # should not raise

    def test_get_revocation_status(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/api-keys/k1/revocation-status"
            return _json_response({
                "data": {
                    "key_id": "k1",
                    "revoked": True,
                    "revoked_at": "2026-03-04T10:00:00Z",
                }
            })

        client = _make_client(handler)
        status = client.keys.get_revocation_status("k1")
        assert status.key_id == "k1"
        assert status.revoked is True
        assert status.revoked_at == "2026-03-04T10:00:00Z"


# ---------------------------------------------------------------------------
# Comments service
# ---------------------------------------------------------------------------

class TestCommentsService:

    def test_create_comment(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "POST"
            assert request.url.path == "/comments"
            body = json.loads(request.content)
            assert body["file_id"] == "f1"
            assert body["content"] == "Great document!"
            return _json_response({
                "data": {
                    "id": "c1",
                    "file_id": "f1",
                    "content": "Great document!",
                    "author_id": "u1",
                    "created_at": "2026-03-04T10:00:00Z",
                    "updated_at": "2026-03-04T10:00:00Z",
                }
            }, status_code=201)

        client = _make_client(handler)
        comment = client.comments.create(CreateCommentRequest(file_id="f1", content="Great document!"))
        assert comment.id == "c1"
        assert comment.file_id == "f1"
        assert comment.content == "Great document!"
        assert comment.author_id == "u1"

    def test_list_comments(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/comments"
            assert "file_id=f1" in str(request.url)
            return _json_response({
                "data": [
                    {"id": "c1", "file_id": "f1", "content": "First comment", "author_id": "u1"},
                    {"id": "c2", "file_id": "f1", "content": "Second comment", "author_id": "u2"},
                ]
            })

        client = _make_client(handler)
        comments = client.comments.list("f1")
        assert len(comments) == 2
        assert comments[0].id == "c1"
        assert comments[1].content == "Second comment"

    def test_get_comment(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/comments/c1"
            return _json_response({
                "data": {"id": "c1", "file_id": "f1", "content": "A comment", "author_id": "u1"}
            })

        client = _make_client(handler)
        comment = client.comments.get("c1")
        assert comment.id == "c1"
        assert comment.content == "A comment"

    def test_update_comment(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "PUT"
            assert request.url.path == "/comments/c1"
            body = json.loads(request.content)
            assert body["content"] == "Updated comment"
            return _json_response({
                "data": {
                    "id": "c1",
                    "file_id": "f1",
                    "content": "Updated comment",
                    "author_id": "u1",
                    "updated_at": "2026-03-04T12:00:00Z",
                }
            })

        client = _make_client(handler)
        comment = client.comments.update("c1", UpdateCommentRequest(content="Updated comment"))
        assert comment.content == "Updated comment"

    def test_delete_comment(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "DELETE"
            assert request.url.path == "/comments/c1"
            return httpx.Response(204)

        client = _make_client(handler)
        client.comments.delete("c1")  # should not raise

    def test_create_reply_comment(self):
        """Test creating a threaded reply by setting parent_id."""
        def handler(request: httpx.Request) -> httpx.Response:
            body = json.loads(request.content)
            assert body["parent_id"] == "c1"
            assert body["file_id"] == "f1"
            return _json_response({
                "data": {
                    "id": "c3",
                    "file_id": "f1",
                    "content": "A reply",
                    "author_id": "u2",
                    "parent_id": "c1",
                }
            }, status_code=201)

        client = _make_client(handler)
        comment = client.comments.create(
            CreateCommentRequest(file_id="f1", content="A reply", parent_id="c1")
        )
        assert comment.parent_id == "c1"


# ---------------------------------------------------------------------------
# Jobs service
# ---------------------------------------------------------------------------

class TestJobsService:

    def test_create_job(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "POST"
            assert request.url.path == "/jobs"
            body = json.loads(request.content)
            assert body["type"] == "bulk_delete"
            return _json_response({
                "data": {
                    "id": "j1",
                    "type": "bulk_delete",
                    "status": "pending",
                    "progress": 0,
                    "created_at": "2026-03-04T10:00:00Z",
                }
            }, status_code=201)

        client = _make_client(handler)
        job = client.jobs.create(CreateJobRequest(type="bulk_delete", params={"file_ids": ["f1", "f2"]}))
        assert job.id == "j1"
        assert job.type == "bulk_delete"
        assert job.status == "pending"

    def test_list_jobs(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/jobs"
            return _json_response({
                "data": [
                    {"id": "j1", "type": "bulk_delete", "status": "completed", "progress": 100},
                    {"id": "j2", "type": "export", "status": "running", "progress": 50},
                ]
            })

        client = _make_client(handler)
        jobs = client.jobs.list()
        assert len(jobs) == 2
        assert jobs[0].status == "completed"
        assert jobs[1].progress == 50

    def test_get_job(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/jobs/j1"
            return _json_response({
                "data": {"id": "j1", "type": "bulk_delete", "status": "completed", "progress": 100}
            })

        client = _make_client(handler)
        job = client.jobs.get("j1")
        assert job.id == "j1"
        assert job.status == "completed"

    def test_cancel_job(self):
        """Cancel uses DELETE method."""
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "DELETE"
            assert request.url.path == "/jobs/j2"
            return httpx.Response(204)

        client = _make_client(handler)
        client.jobs.cancel("j2")  # should not raise


# ---------------------------------------------------------------------------
# Bandwidth service
# ---------------------------------------------------------------------------

class TestBandwidthService:

    def test_get_summary(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/bandwidth"
            return _json_response({
                "data": {
                    "total_upload_bytes": 1048576,
                    "total_download_bytes": 2097152,
                    "period": "2026-03",
                }
            })

        client = _make_client(handler)
        summary = client.bandwidth.get_summary()
        assert summary.total_upload_bytes == 1048576
        assert summary.total_download_bytes == 2097152
        assert summary.period == "2026-03"

    def test_get_daily(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/bandwidth/daily"
            return _json_response({
                "data": [
                    {"date": "2026-03-01", "upload_bytes": 512000, "download_bytes": 1024000},
                    {"date": "2026-03-02", "upload_bytes": 256000, "download_bytes": 768000},
                ]
            })

        client = _make_client(handler)
        daily = client.bandwidth.get_daily()
        assert len(daily) == 2
        assert daily[0].date == "2026-03-01"
        assert daily[0].upload_bytes == 512000
        assert daily[1].download_bytes == 768000


# ---------------------------------------------------------------------------
# Data Export service
# ---------------------------------------------------------------------------

class TestDataExportService:

    def test_export(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/users/u1/export"
            assert request.method == "GET"
            return _json_response({
                "data": {
                    "user_id": "u1",
                    "status": "ready",
                    "url": "https://export.example.com/u1.zip",
                    "expires_at": "2026-03-11T10:00:00Z",
                    "created_at": "2026-03-04T10:00:00Z",
                }
            })

        client = _make_client(handler)
        export = client.data_export.export("u1")
        assert export.user_id == "u1"
        assert export.status == "ready"
        assert export.url == "https://export.example.com/u1.zip"
        assert export.expires_at == "2026-03-11T10:00:00Z"


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

        client = _make_client(handler)
        with pytest.raises(RateLimitError) as exc_info:
            client.files.list()
        assert exc_info.value.retry_after == 30.0
        assert is_rate_limited(exc_info.value)

    def test_rate_limit_error_str(self):
        err = RateLimitError(retry_after=42.0, message="slow down")
        assert "42.0" in str(err)

    def test_rate_limit_error_repr(self):
        err = RateLimitError(retry_after=42.0)
        assert "42.0" in repr(err)

    def test_rate_limit_default_retry_after(self):
        """Without a Retry-After header, default to 60s."""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(429, json={"error": "rate limited"})

        client = _make_client(handler)
        with pytest.raises(RateLimitError) as exc_info:
            client.files.list()
        assert exc_info.value.retry_after == 60.0

    def test_rate_limit_invalid_retry_after(self):
        """Non-numeric Retry-After falls back to 60s."""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                429,
                json={"error": "rate limited"},
                headers={"Retry-After": "not-a-number"},
            )

        client = _make_client(handler)
        with pytest.raises(RateLimitError) as exc_info:
            client.files.list()
        assert exc_info.value.retry_after == 60.0

    def test_not_found_error(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(404, json={"error": "file not found"})

        client = _make_client(handler)
        with pytest.raises(APIError) as exc_info:
            client.files.get("nonexistent")
        assert exc_info.value.status_code == 404
        assert is_not_found(exc_info.value)

    def test_is_not_found_false_for_other_errors(self):
        err = APIError(status_code=500, message="server error")
        assert is_not_found(err) is False

    def test_is_not_found_false_for_non_api_error(self):
        assert is_not_found(ValueError("not an API error")) is False

    def test_is_rate_limited_false_for_non_rate_limit(self):
        err = APIError(status_code=500, message="server error")
        assert is_rate_limited(err) is False

    def test_authentication_error(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(401, json={"error": "invalid api key"})

        client = _make_client(handler, api_key="bad-key")
        with pytest.raises(AuthenticationError) as exc_info:
            client.files.list()
        assert exc_info.value.status_code == 401

    def test_authentication_error_403(self):
        """403 Forbidden should also raise AuthenticationError."""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(403, json={"error": "forbidden"})

        client = _make_client(handler)
        with pytest.raises(AuthenticationError):
            client.files.list()

    def test_generic_api_error(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(500, json={"error": "internal server error"})

        client = _make_client(handler)
        with pytest.raises(APIError) as exc_info:
            client.files.list()
        assert exc_info.value.status_code == 500
        assert "internal server error" in str(exc_info.value)

    def test_api_error_repr(self):
        err = APIError(status_code=502, message="bad gateway")
        assert "502" in repr(err)
        assert "bad gateway" in repr(err)

    def test_error_with_no_json_body(self):
        """API returns a non-JSON error body."""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(503, content=b"Service Unavailable")

        client = _make_client(handler)
        with pytest.raises(APIError) as exc_info:
            client.files.list()
        assert exc_info.value.status_code == 503

    def test_error_with_empty_json_error_field(self):
        """API returns JSON with empty error string -- should fall back to reason phrase."""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(500, json={"error": ""})

        client = _make_client(handler)
        with pytest.raises(APIError) as exc_info:
            client.files.list()
        assert exc_info.value.status_code == 500
        # message should not be empty -- falls back to reason phrase
        assert exc_info.value.message != ""


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

        async with _make_async_client(handler, api_key="async-key") as client:
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

        async with _make_async_client(handler) as client:
            folder = await client.folders.create(CreateFolderRequest(name="Async Folder"))
            assert folder.id == "ad1"

    @pytest.mark.anyio
    async def test_async_error_handling(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(429, json={"error": "slow down"}, headers={"Retry-After": "15"})

        async with _make_async_client(handler) as client:
            with pytest.raises(RateLimitError) as exc_info:
                await client.files.list()
            assert exc_info.value.retry_after == 15.0

    @pytest.mark.anyio
    async def test_async_comments_create(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "POST"
            assert request.url.path == "/comments"
            body = json.loads(request.content)
            assert body["content"] == "Async comment"
            return _json_response({
                "data": {"id": "c1", "file_id": "f1", "content": "Async comment", "author_id": "u1"}
            }, status_code=201)

        async with _make_async_client(handler) as client:
            comment = await client.comments.create(CreateCommentRequest(file_id="f1", content="Async comment"))
            assert comment.id == "c1"

    @pytest.mark.anyio
    async def test_async_comments_list(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            assert "file_id=f1" in str(request.url)
            return _json_response({
                "data": [
                    {"id": "c1", "file_id": "f1", "content": "Comment A", "author_id": "u1"},
                ]
            })

        async with _make_async_client(handler) as client:
            comments = await client.comments.list("f1")
            assert len(comments) == 1

    @pytest.mark.anyio
    async def test_async_comments_update(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "PUT"
            return _json_response({
                "data": {"id": "c1", "file_id": "f1", "content": "Updated async", "author_id": "u1"}
            })

        async with _make_async_client(handler) as client:
            comment = await client.comments.update("c1", UpdateCommentRequest(content="Updated async"))
            assert comment.content == "Updated async"

    @pytest.mark.anyio
    async def test_async_comments_delete(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "DELETE"
            return httpx.Response(204)

        async with _make_async_client(handler) as client:
            await client.comments.delete("c1")

    @pytest.mark.anyio
    async def test_async_jobs_create(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            body = json.loads(request.content)
            assert body["type"] == "export"
            return _json_response({
                "data": {"id": "j1", "type": "export", "status": "pending", "progress": 0}
            }, status_code=201)

        async with _make_async_client(handler) as client:
            job = await client.jobs.create(CreateJobRequest(type="export"))
            assert job.id == "j1"

    @pytest.mark.anyio
    async def test_async_jobs_list(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            return _json_response({
                "data": [{"id": "j1", "type": "export", "status": "completed", "progress": 100}]
            })

        async with _make_async_client(handler) as client:
            jobs = await client.jobs.list()
            assert len(jobs) == 1

    @pytest.mark.anyio
    async def test_async_jobs_cancel(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "DELETE"
            return httpx.Response(204)

        async with _make_async_client(handler) as client:
            await client.jobs.cancel("j1")

    @pytest.mark.anyio
    async def test_async_bandwidth_get_summary(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            return _json_response({
                "data": {"total_upload_bytes": 100, "total_download_bytes": 200, "period": "2026-03"}
            })

        async with _make_async_client(handler) as client:
            summary = await client.bandwidth.get_summary()
            assert summary.total_upload_bytes == 100

    @pytest.mark.anyio
    async def test_async_bandwidth_get_daily(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            return _json_response({
                "data": [{"date": "2026-03-01", "upload_bytes": 10, "download_bytes": 20}]
            })

        async with _make_async_client(handler) as client:
            daily = await client.bandwidth.get_daily()
            assert len(daily) == 1
            assert daily[0].date == "2026-03-01"

    @pytest.mark.anyio
    async def test_async_data_export(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/users/u1/export"
            return _json_response({
                "data": {"user_id": "u1", "status": "ready", "created_at": "2026-03-04T10:00:00Z"}
            })

        async with _make_async_client(handler) as client:
            export = await client.data_export.export("u1")
            assert export.user_id == "u1"
            assert export.status == "ready"

    @pytest.mark.anyio
    async def test_async_keys_instant_revoke(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "POST"
            assert request.url.path == "/api-keys/k1/revoke"
            return httpx.Response(204)

        async with _make_async_client(handler) as client:
            await client.keys.instant_revoke("k1")

    @pytest.mark.anyio
    async def test_async_keys_get_revocation_status(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/api-keys/k1/revocation-status"
            return _json_response({
                "data": {"key_id": "k1", "revoked": False}
            })

        async with _make_async_client(handler) as client:
            status = await client.keys.get_revocation_status("k1")
            assert status.key_id == "k1"
            assert status.revoked is False

    @pytest.mark.anyio
    async def test_async_authentication_error(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(401, json={"error": "unauthorized"})

        async with _make_async_client(handler) as client:
            with pytest.raises(AuthenticationError):
                await client.files.list()

    @pytest.mark.anyio
    async def test_async_not_found_error(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(404, json={"error": "not found"})

        async with _make_async_client(handler) as client:
            with pytest.raises(APIError) as exc_info:
                await client.files.get("missing")
            assert exc_info.value.status_code == 404

    @pytest.mark.anyio
    async def test_async_server_error(self):
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(500, json={"error": "boom"})

        async with _make_async_client(handler) as client:
            with pytest.raises(APIError) as exc_info:
                await client.files.list()
            assert exc_info.value.status_code == 500
