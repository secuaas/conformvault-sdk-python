"""Signatures service for the ConformVault Python SDK."""

from __future__ import annotations

from .client import _AsyncHTTP, _SyncHTTP, _from_dict
from .types import CreateSignatureRequest, SignatureEnvelope


class SignaturesService:
    """Synchronous electronic signature operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def create(self, request: CreateSignatureRequest) -> SignatureEnvelope:
        """Create a new signature envelope."""
        resp = self._http.request_json("POST", "/signatures", body=request)
        return _from_dict(SignatureEnvelope, resp.get("data") if resp else None)

    def get_status(self, envelope_id: str) -> SignatureEnvelope:
        """Get the current status of a signature envelope."""
        resp = self._http.request_json("GET", f"/signatures/{envelope_id}")
        return _from_dict(SignatureEnvelope, resp.get("data") if resp else None)

    def download_signed(self, envelope_id: str) -> bytes:
        """Download the completed signed document."""
        resp = self._http.request_stream("GET", f"/signatures/{envelope_id}/download")
        try:
            return resp.read()
        finally:
            resp.close()

    def revoke(self, envelope_id: str) -> None:
        """Revoke (cancel) a pending signature envelope."""
        self._http.request_json("POST", f"/signatures/{envelope_id}/revoke")


class AsyncSignaturesService:
    """Asynchronous electronic signature operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def create(self, request: CreateSignatureRequest) -> SignatureEnvelope:
        resp = await self._http.request_json("POST", "/signatures", body=request)
        return _from_dict(SignatureEnvelope, resp.get("data") if resp else None)

    async def get_status(self, envelope_id: str) -> SignatureEnvelope:
        resp = await self._http.request_json("GET", f"/signatures/{envelope_id}")
        return _from_dict(SignatureEnvelope, resp.get("data") if resp else None)

    async def download_signed(self, envelope_id: str) -> bytes:
        resp = await self._http.request_stream("GET", f"/signatures/{envelope_id}/download")
        try:
            return await resp.aread()
        finally:
            await resp.aclose()

    async def revoke(self, envelope_id: str) -> None:
        await self._http.request_json("POST", f"/signatures/{envelope_id}/revoke")
