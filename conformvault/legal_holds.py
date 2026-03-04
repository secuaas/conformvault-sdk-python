"""Legal holds service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import List

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import AddLegalHoldFilesRequest, CreateLegalHoldRequest, LegalHold, LegalHoldFile


class LegalHoldsService:
    """Synchronous legal hold operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def create(self, request: CreateLegalHoldRequest) -> LegalHold:
        """Create a legal hold."""
        resp = self._http.request_json("POST", "/legal-holds", body=request)
        return _from_dict(LegalHold, resp.get("data") if resp else None)

    def list(self) -> List[LegalHold]:
        """List all legal holds."""
        resp = self._http.request_json("GET", "/legal-holds")
        return _from_dict_list(LegalHold, resp.get("data", []) if resp else [])

    def get(self, hold_id: str) -> LegalHold:
        """Get a legal hold by ID."""
        resp = self._http.request_json("GET", f"/legal-holds/{hold_id}")
        return _from_dict(LegalHold, resp.get("data") if resp else None)

    def release(self, hold_id: str) -> LegalHold:
        """Release a legal hold."""
        resp = self._http.request_json("POST", f"/legal-holds/{hold_id}/release")
        return _from_dict(LegalHold, resp.get("data") if resp else None)

    def add_files(self, hold_id: str, request: AddLegalHoldFilesRequest) -> List[LegalHoldFile]:
        """Add files to a legal hold."""
        resp = self._http.request_json("POST", f"/legal-holds/{hold_id}/files", body=request)
        return _from_dict_list(LegalHoldFile, resp.get("data", []) if resp else [])

    def remove_file(self, hold_id: str, file_id: str) -> None:
        """Remove a file from a legal hold."""
        self._http.request_json("DELETE", f"/legal-holds/{hold_id}/files/{file_id}")


class AsyncLegalHoldsService:
    """Asynchronous legal hold operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def create(self, request: CreateLegalHoldRequest) -> LegalHold:
        resp = await self._http.request_json("POST", "/legal-holds", body=request)
        return _from_dict(LegalHold, resp.get("data") if resp else None)

    async def list(self) -> List[LegalHold]:
        resp = await self._http.request_json("GET", "/legal-holds")
        return _from_dict_list(LegalHold, resp.get("data", []) if resp else [])

    async def get(self, hold_id: str) -> LegalHold:
        resp = await self._http.request_json("GET", f"/legal-holds/{hold_id}")
        return _from_dict(LegalHold, resp.get("data") if resp else None)

    async def release(self, hold_id: str) -> LegalHold:
        resp = await self._http.request_json("POST", f"/legal-holds/{hold_id}/release")
        return _from_dict(LegalHold, resp.get("data") if resp else None)

    async def add_files(self, hold_id: str, request: AddLegalHoldFilesRequest) -> List[LegalHoldFile]:
        resp = await self._http.request_json("POST", f"/legal-holds/{hold_id}/files", body=request)
        return _from_dict_list(LegalHoldFile, resp.get("data", []) if resp else [])

    async def remove_file(self, hold_id: str, file_id: str) -> None:
        await self._http.request_json("DELETE", f"/legal-holds/{hold_id}/files/{file_id}")
