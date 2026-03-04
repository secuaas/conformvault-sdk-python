"""Webhooks service and signature verification for the ConformVault Python SDK."""

from __future__ import annotations

import hashlib
import hmac
from typing import List

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import RegisterWebhookRequest, RegisterWebhookResponse, WebhookDelivery, WebhookEndpoint


class WebhooksService:
    """Synchronous webhook endpoint management."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def list(self) -> List[WebhookEndpoint]:
        """List all registered webhook endpoints."""
        resp = self._http.request_json("GET", "/webhooks")
        return _from_dict_list(WebhookEndpoint, resp.get("data", []) if resp else [])

    def register(self, request: RegisterWebhookRequest) -> RegisterWebhookResponse:
        """Register a new webhook endpoint. The signing secret is returned once."""
        resp = self._http.request_json("POST", "/webhooks", body=request)
        return _from_dict(RegisterWebhookResponse, resp.get("data") if resp else None)

    def delete(self, webhook_id: str) -> None:
        """Delete a webhook endpoint."""
        self._http.request_json("DELETE", f"/webhooks/{webhook_id}")

    def test(self, webhook_id: str) -> None:
        """Send a test event to a webhook endpoint."""
        self._http.request_json("POST", f"/webhooks/{webhook_id}/test")

    def list_deliveries(self, webhook_id: str) -> List[WebhookDelivery]:
        """List delivery attempts for a webhook endpoint."""
        resp = self._http.request_json("GET", f"/webhooks/{webhook_id}/deliveries")
        return _from_dict_list(WebhookDelivery, resp.get("data", []) if resp else [])

    def get_delivery(self, webhook_id: str, delivery_id: str) -> WebhookDelivery:
        """Get a single webhook delivery by ID."""
        resp = self._http.request_json("GET", f"/webhooks/{webhook_id}/deliveries/{delivery_id}")
        return _from_dict(WebhookDelivery, resp.get("data") if resp else None)

    def replay_delivery(self, webhook_id: str, delivery_id: str) -> None:
        """Replay a webhook delivery."""
        self._http.request_json("POST", f"/webhooks/{webhook_id}/deliveries/{delivery_id}/replay")

    def re_enable(self, webhook_id: str) -> None:
        """Re-enable a disabled webhook endpoint."""
        self._http.request_json("POST", f"/webhooks/{webhook_id}/enable")


class AsyncWebhooksService:
    """Asynchronous webhook endpoint management."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def list(self) -> List[WebhookEndpoint]:
        resp = await self._http.request_json("GET", "/webhooks")
        return _from_dict_list(WebhookEndpoint, resp.get("data", []) if resp else [])

    async def register(self, request: RegisterWebhookRequest) -> RegisterWebhookResponse:
        resp = await self._http.request_json("POST", "/webhooks", body=request)
        return _from_dict(RegisterWebhookResponse, resp.get("data") if resp else None)

    async def delete(self, webhook_id: str) -> None:
        await self._http.request_json("DELETE", f"/webhooks/{webhook_id}")

    async def test(self, webhook_id: str) -> None:
        await self._http.request_json("POST", f"/webhooks/{webhook_id}/test")

    async def list_deliveries(self, webhook_id: str) -> List[WebhookDelivery]:
        resp = await self._http.request_json("GET", f"/webhooks/{webhook_id}/deliveries")
        return _from_dict_list(WebhookDelivery, resp.get("data", []) if resp else [])

    async def get_delivery(self, webhook_id: str, delivery_id: str) -> WebhookDelivery:
        resp = await self._http.request_json("GET", f"/webhooks/{webhook_id}/deliveries/{delivery_id}")
        return _from_dict(WebhookDelivery, resp.get("data") if resp else None)

    async def replay_delivery(self, webhook_id: str, delivery_id: str) -> None:
        await self._http.request_json("POST", f"/webhooks/{webhook_id}/deliveries/{delivery_id}/replay")

    async def re_enable(self, webhook_id: str) -> None:
        await self._http.request_json("POST", f"/webhooks/{webhook_id}/enable")


def verify_webhook_signature(payload: bytes | str, signature_header: str, secret: str) -> bool:
    """Verify that a webhook payload was signed by ConformVault.

    The signature header format is ``t=<timestamp>,s0=<hmac_hex>``.
    The HMAC is computed as ``HMAC-SHA256(timestamp + "." + payload_body, secret)``.

    For backwards compatibility, if the header does not contain the ``t=...``
    prefix, it is treated as a raw HMAC hex digest (matching the Go SDK).

    Args:
        payload: The raw request body (bytes or str).
        signature_header: The ``X-Webhook-Signature`` (or ``X-ConformVault-Signature``) header value.
        secret: The webhook signing secret.

    Returns:
        ``True`` if the signature is valid.
    """
    if isinstance(payload, str):
        payload = payload.encode("utf-8")

    # Parse structured header: t=<ts>,s0=<sig>
    if "," in signature_header and signature_header.startswith("t="):
        parts: dict[str, str] = {}
        for segment in signature_header.split(","):
            if "=" in segment:
                key, _, value = segment.partition("=")
                parts[key.strip()] = value.strip()

        timestamp = parts.get("t", "")
        provided_sig = parts.get("s0", "")
        if not timestamp or not provided_sig:
            return False

        # Compute expected: HMAC-SHA256(timestamp + "." + payload, secret)
        signed_content = f"{timestamp}.".encode("utf-8") + payload
        mac = hmac.new(secret.encode("utf-8"), signed_content, hashlib.sha256)
        expected_sig = mac.hexdigest()
        return hmac.compare_digest(provided_sig, expected_sig)

    # Fallback: raw HMAC hex digest (Go SDK compatibility)
    mac = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256)
    expected_sig = mac.hexdigest()
    return hmac.compare_digest(signature_header, expected_sig)
