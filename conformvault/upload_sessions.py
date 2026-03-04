"""Upload sessions service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import Union

from .client import _AsyncHTTP, _SyncHTTP, _build_headers, _from_dict, _handle_error_response
from .types import CreateUploadSessionRequest, File, UploadSession


class UploadSessionsService:
    """Synchronous chunked upload session operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def create(self, request: CreateUploadSessionRequest) -> UploadSession:
        """Create a new chunked upload session."""
        resp = self._http.request_json("POST", "/upload-sessions", body=request)
        return _from_dict(UploadSession, resp.get("data") if resp else None)

    def upload_chunk(self, session_id: str, chunk_number: int, data: Union[bytes, bytearray]) -> None:
        """Upload a single chunk of data to an upload session."""
        url = self._http._base_url + f"/upload-sessions/{session_id}/chunks/{chunk_number}"
        headers = _build_headers(self._http._api_key)
        headers["Content-Type"] = "application/octet-stream"
        resp = self._http._client.put(url, content=data, headers=headers)
        if resp.status_code >= 400:
            _handle_error_response(resp)

    def get_status(self, session_id: str) -> UploadSession:
        """Get the status of an upload session."""
        resp = self._http.request_json("GET", f"/upload-sessions/{session_id}")
        return _from_dict(UploadSession, resp.get("data") if resp else None)

    def complete(self, session_id: str) -> File:
        """Complete an upload session and finalize the file."""
        resp = self._http.request_json("POST", f"/upload-sessions/{session_id}/complete")
        return _from_dict(File, resp.get("data") if resp else None)

    def cancel(self, session_id: str) -> None:
        """Cancel an upload session."""
        self._http.request_json("DELETE", f"/upload-sessions/{session_id}")


class AsyncUploadSessionsService:
    """Asynchronous chunked upload session operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def create(self, request: CreateUploadSessionRequest) -> UploadSession:
        resp = await self._http.request_json("POST", "/upload-sessions", body=request)
        return _from_dict(UploadSession, resp.get("data") if resp else None)

    async def upload_chunk(self, session_id: str, chunk_number: int, data: Union[bytes, bytearray]) -> None:
        url = self._http._base_url + f"/upload-sessions/{session_id}/chunks/{chunk_number}"
        headers = _build_headers(self._http._api_key)
        headers["Content-Type"] = "application/octet-stream"
        resp = await self._http._client.put(url, content=data, headers=headers)
        if resp.status_code >= 400:
            _handle_error_response(resp)

    async def get_status(self, session_id: str) -> UploadSession:
        resp = await self._http.request_json("GET", f"/upload-sessions/{session_id}")
        return _from_dict(UploadSession, resp.get("data") if resp else None)

    async def complete(self, session_id: str) -> File:
        resp = await self._http.request_json("POST", f"/upload-sessions/{session_id}/complete")
        return _from_dict(File, resp.get("data") if resp else None)

    async def cancel(self, session_id: str) -> None:
        await self._http.request_json("DELETE", f"/upload-sessions/{session_id}")
