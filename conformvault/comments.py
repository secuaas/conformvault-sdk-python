"""Comments service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import List

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import Comment, CreateCommentRequest, UpdateCommentRequest


class CommentsService:
    """Synchronous file comment operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def create(self, request: CreateCommentRequest) -> Comment:
        """Create a comment on a file."""
        resp = self._http.request_json("POST", "/comments", body=request)
        return _from_dict(Comment, resp.get("data") if resp else None)

    def list(self, file_id: str) -> List[Comment]:
        """List all comments on a file."""
        resp = self._http.request_json("GET", "/comments", params={"file_id": file_id})
        return _from_dict_list(Comment, resp.get("data", []) if resp else [])

    def get(self, comment_id: str) -> Comment:
        """Get a single comment by ID."""
        resp = self._http.request_json("GET", f"/comments/{comment_id}")
        return _from_dict(Comment, resp.get("data") if resp else None)

    def update(self, comment_id: str, request: UpdateCommentRequest) -> Comment:
        """Update a comment."""
        resp = self._http.request_json("PUT", f"/comments/{comment_id}", body=request)
        return _from_dict(Comment, resp.get("data") if resp else None)

    def delete(self, comment_id: str) -> None:
        """Delete a comment."""
        self._http.request_json("DELETE", f"/comments/{comment_id}")

    def get_replies(self, comment_id: str) -> List[Comment]:
        """Get replies to a comment."""
        resp = self._http.request_json("GET", f"/comments/{comment_id}/replies")
        return _from_dict_list(Comment, resp.get("data", []) if resp else [])


class AsyncCommentsService:
    """Asynchronous file comment operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def create(self, request: CreateCommentRequest) -> Comment:
        resp = await self._http.request_json("POST", "/comments", body=request)
        return _from_dict(Comment, resp.get("data") if resp else None)

    async def list(self, file_id: str) -> List[Comment]:
        resp = await self._http.request_json("GET", "/comments", params={"file_id": file_id})
        return _from_dict_list(Comment, resp.get("data", []) if resp else [])

    async def get(self, comment_id: str) -> Comment:
        resp = await self._http.request_json("GET", f"/comments/{comment_id}")
        return _from_dict(Comment, resp.get("data") if resp else None)

    async def update(self, comment_id: str, request: UpdateCommentRequest) -> Comment:
        resp = await self._http.request_json("PUT", f"/comments/{comment_id}", body=request)
        return _from_dict(Comment, resp.get("data") if resp else None)

    async def delete(self, comment_id: str) -> None:
        await self._http.request_json("DELETE", f"/comments/{comment_id}")

    async def get_replies(self, comment_id: str) -> List[Comment]:
        resp = await self._http.request_json("GET", f"/comments/{comment_id}/replies")
        return _from_dict_list(Comment, resp.get("data", []) if resp else [])
