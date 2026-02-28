"""Trash / recycle bin operations service."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional

from .client import _from_dict_list
from .types import File

if TYPE_CHECKING:
    from .client import _AsyncHTTP, _SyncHTTP


class TrashService:
    """Synchronous trash operations."""

    def __init__(self, http: "_SyncHTTP") -> None:
        self._http = http

    def list(self, *, page: int = 1, limit: int = 50) -> Dict:
        """List all trashed files.

        Returns:
            Dict with "data" (list of File) and "pagination".
        """
        params = {"page": str(page), "limit": str(limit)}
        data = self._http.request_json("GET", "/trash", params=params)
        return {
            "data": _from_dict_list(File, data.get("data", []) if data else []),
            "pagination": data.get("pagination", {}) if data else {},
        }

    def restore(self, file_id: str) -> None:
        """Restore a file from the trash."""
        self._http.request_json("POST", f"/trash/{file_id}/restore")

    def delete(self, file_id: str) -> None:
        """Permanently delete a file from the trash."""
        self._http.request_json("DELETE", f"/trash/{file_id}")

    def empty(self) -> Dict:
        """Empty the entire trash. Returns message and files_deleted count."""
        data = self._http.request_json("DELETE", "/trash")
        return data or {}


class AsyncTrashService:
    """Asynchronous trash operations."""

    def __init__(self, http: "_AsyncHTTP") -> None:
        self._http = http

    async def list(self, *, page: int = 1, limit: int = 50) -> Dict:
        params = {"page": str(page), "limit": str(limit)}
        data = await self._http.request_json("GET", "/trash", params=params)
        return {
            "data": _from_dict_list(File, data.get("data", []) if data else []),
            "pagination": data.get("pagination", {}) if data else {},
        }

    async def restore(self, file_id: str) -> None:
        await self._http.request_json("POST", f"/trash/{file_id}/restore")

    async def delete(self, file_id: str) -> None:
        await self._http.request_json("DELETE", f"/trash/{file_id}")

    async def empty(self) -> Dict:
        data = await self._http.request_json("DELETE", "/trash")
        return data or {}
