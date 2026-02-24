"""Share links service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import Dict, List

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import CreateShareLinkRequest, ShareLink


class ShareLinksService:
    """Synchronous share link operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def list(self, *, page: int = 0, limit: int = 0) -> List[ShareLink]:
        """List share links."""
        params: Dict[str, str] = {}
        if page > 0:
            params["page"] = str(page)
        if limit > 0:
            params["limit"] = str(limit)

        resp = self._http.request_json("GET", "/sharelinks", params=params or None)
        return _from_dict_list(ShareLink, resp.get("data", []) if resp else [])

    def create(self, request: CreateShareLinkRequest) -> ShareLink:
        """Create a new share link."""
        resp = self._http.request_json("POST", "/sharelinks", body=request)
        return _from_dict(ShareLink, resp.get("data") if resp else None)

    def delete(self, share_link_id: str) -> None:
        """Delete a share link by ID."""
        self._http.request_json("DELETE", f"/sharelinks/{share_link_id}")


class AsyncShareLinksService:
    """Asynchronous share link operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def list(self, *, page: int = 0, limit: int = 0) -> List[ShareLink]:
        params: Dict[str, str] = {}
        if page > 0:
            params["page"] = str(page)
        if limit > 0:
            params["limit"] = str(limit)

        resp = await self._http.request_json("GET", "/sharelinks", params=params or None)
        return _from_dict_list(ShareLink, resp.get("data", []) if resp else [])

    async def create(self, request: CreateShareLinkRequest) -> ShareLink:
        resp = await self._http.request_json("POST", "/sharelinks", body=request)
        return _from_dict(ShareLink, resp.get("data") if resp else None)

    async def delete(self, share_link_id: str) -> None:
        await self._http.request_json("DELETE", f"/sharelinks/{share_link_id}")
