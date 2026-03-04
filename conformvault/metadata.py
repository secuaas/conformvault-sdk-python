"""Metadata and tags service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import Dict, List

from .client import _AsyncHTTP, _SyncHTTP, _from_dict_list
from .types import AddTagsRequest, File, FileTag, SetMetadataRequest


class MetadataService:
    """Synchronous file metadata and tag operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def add_tags(self, file_id: str, request: AddTagsRequest) -> List[FileTag]:
        """Add tags to a file."""
        resp = self._http.request_json("POST", f"/files/{file_id}/tags", body=request)
        return _from_dict_list(FileTag, resp.get("data", []) if resp else [])

    def remove_tag(self, file_id: str, tag: str) -> None:
        """Remove a tag from a file."""
        self._http.request_json("DELETE", f"/files/{file_id}/tags/{tag}")

    def get_tags(self, file_id: str) -> List[FileTag]:
        """Get all tags for a file."""
        resp = self._http.request_json("GET", f"/files/{file_id}/tags")
        return _from_dict_list(FileTag, resp.get("data", []) if resp else [])

    def list_by_tag(self, tag: str) -> List[File]:
        """List files that have the given tag."""
        resp = self._http.request_json("GET", f"/files/by-tag/{tag}")
        return _from_dict_list(File, resp.get("data", []) if resp else [])

    def set_metadata(self, file_id: str, request: SetMetadataRequest) -> Dict[str, str]:
        """Set custom metadata on a file."""
        resp = self._http.request_json("PATCH", f"/files/{file_id}/metadata", body=request)
        return resp.get("data", {}) if resp else {}

    def get_metadata(self, file_id: str) -> Dict[str, str]:
        """Get custom metadata for a file."""
        resp = self._http.request_json("GET", f"/files/{file_id}/metadata")
        return resp.get("data", {}) if resp else {}

    def delete_metadata_key(self, file_id: str, key: str) -> None:
        """Delete a single metadata key from a file."""
        self._http.request_json("DELETE", f"/files/{file_id}/metadata/{key}")


class AsyncMetadataService:
    """Asynchronous file metadata and tag operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def add_tags(self, file_id: str, request: AddTagsRequest) -> List[FileTag]:
        resp = await self._http.request_json("POST", f"/files/{file_id}/tags", body=request)
        return _from_dict_list(FileTag, resp.get("data", []) if resp else [])

    async def remove_tag(self, file_id: str, tag: str) -> None:
        await self._http.request_json("DELETE", f"/files/{file_id}/tags/{tag}")

    async def get_tags(self, file_id: str) -> List[FileTag]:
        resp = await self._http.request_json("GET", f"/files/{file_id}/tags")
        return _from_dict_list(FileTag, resp.get("data", []) if resp else [])

    async def list_by_tag(self, tag: str) -> List[File]:
        resp = await self._http.request_json("GET", f"/files/by-tag/{tag}")
        return _from_dict_list(File, resp.get("data", []) if resp else [])

    async def set_metadata(self, file_id: str, request: SetMetadataRequest) -> Dict[str, str]:
        resp = await self._http.request_json("PATCH", f"/files/{file_id}/metadata", body=request)
        return resp.get("data", {}) if resp else {}

    async def get_metadata(self, file_id: str) -> Dict[str, str]:
        resp = await self._http.request_json("GET", f"/files/{file_id}/metadata")
        return resp.get("data", {}) if resp else {}

    async def delete_metadata_key(self, file_id: str, key: str) -> None:
        await self._http.request_json("DELETE", f"/files/{file_id}/metadata/{key}")
