"""File version operations service."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from .client import _from_dict, _from_dict_list
from .types import FileVersion

if TYPE_CHECKING:
    from .client import _AsyncHTTP, _SyncHTTP


class VersionsService:
    """Synchronous file version operations."""

    def __init__(self, http: "_SyncHTTP") -> None:
        self._http = http

    def list(self, file_id: str) -> List[FileVersion]:
        """List all versions of a file."""
        data = self._http.request_json("GET", f"/files/{file_id}/versions")
        return _from_dict_list(FileVersion, data.get("data", []) if data else [])

    def get(self, file_id: str, version_id: str) -> FileVersion:
        """Get a specific file version."""
        data = self._http.request_json("GET", f"/files/{file_id}/versions/{version_id}")
        return _from_dict(FileVersion, data.get("data", {}) if data else {})

    def restore(self, file_id: str, version_id: str) -> None:
        """Restore a file to a previous version."""
        self._http.request_json("POST", f"/files/{file_id}/versions/{version_id}/restore")

    def delete(self, file_id: str, version_id: str) -> None:
        """Permanently delete a file version."""
        self._http.request_json("DELETE", f"/files/{file_id}/versions/{version_id}")


class AsyncVersionsService:
    """Asynchronous file version operations."""

    def __init__(self, http: "_AsyncHTTP") -> None:
        self._http = http

    async def list(self, file_id: str) -> List[FileVersion]:
        data = await self._http.request_json("GET", f"/files/{file_id}/versions")
        return _from_dict_list(FileVersion, data.get("data", []) if data else [])

    async def get(self, file_id: str, version_id: str) -> FileVersion:
        data = await self._http.request_json("GET", f"/files/{file_id}/versions/{version_id}")
        return _from_dict(FileVersion, data.get("data", {}) if data else {})

    async def restore(self, file_id: str, version_id: str) -> None:
        await self._http.request_json("POST", f"/files/{file_id}/versions/{version_id}/restore")

    async def delete(self, file_id: str, version_id: str) -> None:
        await self._http.request_json("DELETE", f"/files/{file_id}/versions/{version_id}")
