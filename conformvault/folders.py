"""Folders service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import Dict, List, Optional

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import CreateFolderRequest, Folder


class FoldersService:
    """Synchronous folder operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def list(
        self,
        *,
        parent_id: Optional[str] = None,
        page: int = 0,
        limit: int = 0,
    ) -> List[Folder]:
        """List folders, optionally filtered by parent."""
        params: Dict[str, str] = {}
        if parent_id is not None:
            params["parent_id"] = parent_id
        if page > 0:
            params["page"] = str(page)
        if limit > 0:
            params["limit"] = str(limit)

        resp = self._http.request_json("GET", "/folders", params=params or None)
        return _from_dict_list(Folder, resp.get("data", []) if resp else [])

    def get(self, folder_id: str) -> Folder:
        """Get a single folder by ID."""
        resp = self._http.request_json("GET", f"/folders/{folder_id}")
        return _from_dict(Folder, resp.get("data") if resp else None)

    def create(self, request: CreateFolderRequest) -> Folder:
        """Create a new folder."""
        resp = self._http.request_json("POST", "/folders", body=request)
        return _from_dict(Folder, resp.get("data") if resp else None)

    def delete(self, folder_id: str) -> None:
        """Delete a folder by ID."""
        self._http.request_json("DELETE", f"/folders/{folder_id}")


class AsyncFoldersService:
    """Asynchronous folder operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def list(
        self,
        *,
        parent_id: Optional[str] = None,
        page: int = 0,
        limit: int = 0,
    ) -> List[Folder]:
        params: Dict[str, str] = {}
        if parent_id is not None:
            params["parent_id"] = parent_id
        if page > 0:
            params["page"] = str(page)
        if limit > 0:
            params["limit"] = str(limit)

        resp = await self._http.request_json("GET", "/folders", params=params or None)
        return _from_dict_list(Folder, resp.get("data", []) if resp else [])

    async def get(self, folder_id: str) -> Folder:
        resp = await self._http.request_json("GET", f"/folders/{folder_id}")
        return _from_dict(Folder, resp.get("data") if resp else None)

    async def create(self, request: CreateFolderRequest) -> Folder:
        resp = await self._http.request_json("POST", "/folders", body=request)
        return _from_dict(Folder, resp.get("data") if resp else None)

    async def delete(self, folder_id: str) -> None:
        await self._http.request_json("DELETE", f"/folders/{folder_id}")
