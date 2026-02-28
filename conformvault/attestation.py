"""Attestation service for the ConformVault Python SDK."""

from __future__ import annotations

from .client import _AsyncHTTP, _SyncHTTP


class AttestationService:
    """Synchronous Loi 25 attestation operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def generate_loi25(self) -> bytes:
        """Generate and download a Loi 25 compliance attestation PDF.

        Returns:
            Raw PDF bytes for the attestation document.
        """
        resp = self._http.request_stream("GET", "/attestation/loi25")
        try:
            return resp.read()
        finally:
            resp.close()


class AsyncAttestationService:
    """Asynchronous Loi 25 attestation operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def generate_loi25(self) -> bytes:
        """Generate and download a Loi 25 compliance attestation PDF.

        Returns:
            Raw PDF bytes for the attestation document.
        """
        resp = await self._http.request_stream("GET", "/attestation/loi25")
        try:
            return await resp.aread()
        finally:
            await resp.aclose()
