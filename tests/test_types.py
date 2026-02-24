"""Tests for data models (types)."""

from __future__ import annotations

import dataclasses

from conformvault import (
    APIKey,
    AuditEntry,
    CreateAPIKeyRequest,
    CreateAPIKeyResponse,
    CreateFolderRequest,
    CreateShareLinkRequest,
    CreateSignatureRequest,
    CreateSignatureSigner,
    File,
    Folder,
    RegisterWebhookRequest,
    RegisterWebhookResponse,
    ShareLink,
    SignatureEnvelope,
    UploadResult,
    WebhookEndpoint,
)
from conformvault.client import _from_dict, _from_dict_list


class TestDataclassDefaults:
    """All dataclasses should be instantiable with zero arguments."""

    def test_file_defaults(self):
        f = File()
        assert f.id == ""
        assert f.folder_id is None

    def test_upload_result_defaults(self):
        u = UploadResult()
        assert u.id == ""

    def test_folder_defaults(self):
        f = Folder()
        assert f.parent_id is None

    def test_share_link_defaults(self):
        sl = ShareLink()
        assert sl.is_active is False

    def test_signature_envelope_defaults(self):
        se = SignatureEnvelope()
        assert se.message is None

    def test_webhook_endpoint_defaults(self):
        we = WebhookEndpoint()
        assert we.events == []

    def test_api_key_defaults(self):
        ak = APIKey()
        assert ak.scopes == []
        assert ak.expires_at is None


class TestFromDict:
    """Test the _from_dict helper that converts dicts to dataclasses."""

    def test_basic_file(self):
        data = {"id": "f1", "name": "test.pdf", "size": 1024}
        f = _from_dict(File, data)
        assert f.id == "f1"
        assert f.name == "test.pdf"
        assert f.size == 1024
        assert f.folder_id is None  # not in input, uses default

    def test_ignores_unknown_keys(self):
        data = {"id": "f1", "name": "test.pdf", "unknown_field": "ignored"}
        f = _from_dict(File, data)
        assert f.id == "f1"
        assert not hasattr(f, "unknown_field")

    def test_from_dict_list(self):
        items = [
            {"id": "f1", "name": "a.pdf"},
            {"id": "f2", "name": "b.pdf"},
        ]
        result = _from_dict_list(File, items)
        assert len(result) == 2
        assert result[0].id == "f1"
        assert result[1].id == "f2"

    def test_from_dict_list_empty(self):
        result = _from_dict_list(File, [])
        assert result == []

    def test_from_dict_list_non_list(self):
        result = _from_dict_list(File, None)
        assert result == []

    def test_from_dict_none(self):
        f = _from_dict(File, None)
        assert f.id == ""

    def test_nested_signers(self):
        """CreateSignatureRequest with nested signer dicts."""
        data = {
            "file_id": "f1",
            "subject": "Sign here",
            "signers": [
                {"email": "a@b.com", "name": "Alice", "role": "signer", "sign_order": 1},
            ],
        }
        req = _from_dict(CreateSignatureRequest, data)
        assert req.file_id == "f1"
        # Note: nested signers come as dicts, not CreateSignatureSigner instances,
        # because _from_dict doesn't recurse into list fields.
        assert len(req.signers) == 1


class TestDataclassAsDict:
    """Verify dataclasses can round-trip to dicts."""

    def test_create_folder_request(self):
        req = CreateFolderRequest(name="Docs", parent_id="p1")
        d = dataclasses.asdict(req)
        assert d == {"name": "Docs", "parent_id": "p1"}

    def test_create_share_link_request(self):
        req = CreateShareLinkRequest(file_id="f1", type="download", expires_in=3600)
        d = dataclasses.asdict(req)
        assert d["file_id"] == "f1"
        assert d["expires_in"] == 3600
        assert d["password"] is None

    def test_create_api_key_request(self):
        req = CreateAPIKeyRequest(name="Test", environment="test", scopes=["files:read", "files:write"])
        d = dataclasses.asdict(req)
        assert d["scopes"] == ["files:read", "files:write"]
