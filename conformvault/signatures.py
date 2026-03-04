"""Signatures service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import List

from .client import _AsyncHTTP, _SyncHTTP, _from_dict
from .types import (
    AnalyzePDFRequest,
    CreateSignatureRequest,
    EmbeddedSignLinkResponse,
    PDFAnalysisResult,
    SignatureEnvelope,
)


class SignaturesService:
    """Synchronous electronic signature operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def list(self) -> List[SignatureEnvelope]:
        """List all signature envelopes for the organization."""
        resp = self._http.request_json("GET", "/signatures")
        items = resp.get("data") if resp else []
        return [_from_dict(SignatureEnvelope, item) for item in (items or [])]

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

    def download_audit_trail(self, envelope_id: str) -> bytes:
        """Download the audit trail (completion certificate) PDF."""
        resp = self._http.request_stream("GET", f"/signatures/{envelope_id}/audit-trail")
        try:
            return resp.read()
        finally:
            resp.close()

    def revoke(self, envelope_id: str) -> None:
        """Revoke (cancel) a pending signature envelope."""
        self._http.request_json("POST", f"/signatures/{envelope_id}/revoke")

    def analyze_pdf(self, request: AnalyzePDFRequest) -> PDFAnalysisResult:
        """Analyze a PDF to detect suggested signature field placements."""
        resp = self._http.request_json("POST", "/signatures/analyze", body=request)
        return _from_dict(PDFAnalysisResult, resp.get("data") if resp else None)

    def preview_pdf(self, file_id: str) -> bytes:
        """Download a PDF preview for signature placement."""
        resp = self._http.request_stream("GET", f"/signatures/preview-pdf?file_id={file_id}")
        try:
            return resp.read()
        finally:
            resp.close()

    def get_embedded_sign_link(self, envelope_id: str, signer_email: str, redirect_url: str = "") -> EmbeddedSignLinkResponse:
        """Get an embedded signing link for a signer."""
        from urllib.parse import urlencode
        params = {"signer_email": signer_email}
        if redirect_url:
            params["redirect_url"] = redirect_url
        resp = self._http.request_json("GET", f"/signatures/{envelope_id}/embed-sign?{urlencode(params)}")
        return _from_dict(EmbeddedSignLinkResponse, resp if resp else None)


class AsyncSignaturesService:
    """Asynchronous electronic signature operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def list(self) -> List[SignatureEnvelope]:
        """List all signature envelopes for the organization."""
        resp = await self._http.request_json("GET", "/signatures")
        items = resp.get("data") if resp else []
        return [_from_dict(SignatureEnvelope, item) for item in (items or [])]

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

    async def download_audit_trail(self, envelope_id: str) -> bytes:
        """Download the audit trail (completion certificate) PDF."""
        resp = await self._http.request_stream("GET", f"/signatures/{envelope_id}/audit-trail")
        try:
            return await resp.aread()
        finally:
            await resp.aclose()

    async def revoke(self, envelope_id: str) -> None:
        await self._http.request_json("POST", f"/signatures/{envelope_id}/revoke")

    async def analyze_pdf(self, request: AnalyzePDFRequest) -> PDFAnalysisResult:
        """Analyze a PDF to detect suggested signature field placements."""
        resp = await self._http.request_json("POST", "/signatures/analyze", body=request)
        return _from_dict(PDFAnalysisResult, resp.get("data") if resp else None)

    async def preview_pdf(self, file_id: str) -> bytes:
        """Download a PDF preview for signature placement."""
        resp = await self._http.request_stream("GET", f"/signatures/preview-pdf?file_id={file_id}")
        try:
            return await resp.aread()
        finally:
            await resp.aclose()

    async def get_embedded_sign_link(self, envelope_id: str, signer_email: str, redirect_url: str = "") -> EmbeddedSignLinkResponse:
        """Get an embedded signing link for a signer."""
        from urllib.parse import urlencode
        params = {"signer_email": signer_email}
        if redirect_url:
            params["redirect_url"] = redirect_url
        resp = await self._http.request_json("GET", f"/signatures/{envelope_id}/embed-sign?{urlencode(params)}")
        return _from_dict(EmbeddedSignLinkResponse, resp if resp else None)
