"""Files service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import Any, BinaryIO, Dict, List, Optional, Union

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import File, UploadResult


class FilesService:
    """Synchronous file operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def list(
        self,
        *,
        folder_id: Optional[str] = None,
        page: int = 0,
        limit: int = 0,
    ) -> List[File]:
        """List files, optionally filtered by folder."""
        params: Dict[str, str] = {}
        if folder_id is not None:
            params["folder_id"] = folder_id
        if page > 0:
            params["page"] = str(page)
        if limit > 0:
            params["limit"] = str(limit)

        resp = self._http.request_json("GET", "/files", params=params or None)
        return _from_dict_list(File, resp.get("data", []) if resp else [])

    def get(self, file_id: str) -> File:
        """Get a single file by ID."""
        resp = self._http.request_json("GET", f"/files/{file_id}")
        return _from_dict(File, resp.get("data") if resp else None)

    def upload(
        self,
        file: Union[BinaryIO, bytes],
        filename: str,
        *,
        folder_id: Optional[str] = None,
    ) -> UploadResult:
        """Upload a file via multipart form-data."""
        extra: Dict[str, str] = {}
        if folder_id is not None:
            extra["folder_id"] = folder_id
        resp = self._http.upload_file("/files", file, filename, extra_fields=extra or None)
        return _from_dict(UploadResult, resp.get("data") if resp else None)

    def download(self, file_id: str) -> bytes:
        """Download a file and return its bytes."""
        resp = self._http.request_stream("GET", f"/files/{file_id}/download")
        try:
            return resp.read()
        finally:
            resp.close()

    def delete(self, file_id: str) -> None:
        """Delete a file by ID."""
        self._http.request_json("DELETE", f"/files/{file_id}")

    def get_thumbnail(self, file_id: str) -> Any:
        """Get a thumbnail for a file. Returns a streaming ``httpx.Response``."""
        return self._http.request_stream("GET", f"/files/{file_id}/thumbnail")

    def get_scan_report(self, file_id: str) -> Any:
        """Get the antivirus scan report for a file."""
        resp = self._http.request_json("GET", f"/files/{file_id}/scan-report")
        return resp.get("data") if resp else None


class AsyncFilesService:
    """Asynchronous file operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def list(
        self,
        *,
        folder_id: Optional[str] = None,
        page: int = 0,
        limit: int = 0,
    ) -> List[File]:
        params: Dict[str, str] = {}
        if folder_id is not None:
            params["folder_id"] = folder_id
        if page > 0:
            params["page"] = str(page)
        if limit > 0:
            params["limit"] = str(limit)

        resp = await self._http.request_json("GET", "/files", params=params or None)
        return _from_dict_list(File, resp.get("data", []) if resp else [])

    async def get(self, file_id: str) -> File:
        resp = await self._http.request_json("GET", f"/files/{file_id}")
        return _from_dict(File, resp.get("data") if resp else None)

    async def upload(
        self,
        file: Union[BinaryIO, bytes],
        filename: str,
        *,
        folder_id: Optional[str] = None,
    ) -> UploadResult:
        extra: Dict[str, str] = {}
        if folder_id is not None:
            extra["folder_id"] = folder_id
        resp = await self._http.upload_file("/files", file, filename, extra_fields=extra or None)
        return _from_dict(UploadResult, resp.get("data") if resp else None)

    async def download(self, file_id: str) -> bytes:
        resp = await self._http.request_stream("GET", f"/files/{file_id}/download")
        try:
            return await resp.aread()
        finally:
            await resp.aclose()

    async def delete(self, file_id: str) -> None:
        await self._http.request_json("DELETE", f"/files/{file_id}")

    async def get_thumbnail(self, file_id: str) -> Any:
        return await self._http.request_stream("GET", f"/files/{file_id}/thumbnail")

    async def get_scan_report(self, file_id: str) -> Any:
        resp = await self._http.request_json("GET", f"/files/{file_id}/scan-report")
        return resp.get("data") if resp else None
