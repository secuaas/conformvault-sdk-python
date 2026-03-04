"""Folder permissions service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import List

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import FolderPermission, SetFolderPermissionRequest


class PermissionsService:
    """Synchronous folder permission operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def set(self, folder_id: str, request: SetFolderPermissionRequest) -> FolderPermission:
        """Set a permission on a folder."""
        resp = self._http.request_json("POST", f"/folders/{folder_id}/permissions", body=request)
        return _from_dict(FolderPermission, resp.get("data") if resp else None)

    def get(self, folder_id: str) -> List[FolderPermission]:
        """Get all permissions for a folder."""
        resp = self._http.request_json("GET", f"/folders/{folder_id}/permissions")
        return _from_dict_list(FolderPermission, resp.get("data", []) if resp else [])

    def revoke(self, folder_id: str, user_id: str) -> None:
        """Revoke a user's permission on a folder."""
        self._http.request_json("DELETE", f"/folders/{folder_id}/permissions/{user_id}")


class AsyncPermissionsService:
    """Asynchronous folder permission operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def set(self, folder_id: str, request: SetFolderPermissionRequest) -> FolderPermission:
        resp = await self._http.request_json("POST", f"/folders/{folder_id}/permissions", body=request)
        return _from_dict(FolderPermission, resp.get("data") if resp else None)

    async def get(self, folder_id: str) -> List[FolderPermission]:
        resp = await self._http.request_json("GET", f"/folders/{folder_id}/permissions")
        return _from_dict_list(FolderPermission, resp.get("data", []) if resp else [])

    async def revoke(self, folder_id: str, user_id: str) -> None:
        await self._http.request_json("DELETE", f"/folders/{folder_id}/permissions/{user_id}")
