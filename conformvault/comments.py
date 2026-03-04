"""Comments service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import List

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import Comment, CreateCommentRequest, UpdateCommentRequest


class CommentsService:
    """Synchronous file comment operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def create(self, file_id: str, request: CreateCommentRequest) -> Comment:
        """Create a comment on a file."""
        resp = self._http.request_json("POST", f"/files/{file_id}/comments", body=request)
        return _from_dict(Comment, resp.get("data") if resp else None)

    def list(self, file_id: str) -> List[Comment]:
        """List all comments on a file."""
        resp = self._http.request_json("GET", f"/files/{file_id}/comments")
        return _from_dict_list(Comment, resp.get("data", []) if resp else [])

    def get(self, file_id: str, comment_id: str) -> Comment:
        """Get a single comment by ID."""
        resp = self._http.request_json("GET", f"/files/{file_id}/comments/{comment_id}")
        return _from_dict(Comment, resp.get("data") if resp else None)

    def update(self, file_id: str, comment_id: str, request: UpdateCommentRequest) -> Comment:
        """Update a comment."""
        resp = self._http.request_json("PATCH", f"/files/{file_id}/comments/{comment_id}", body=request)
        return _from_dict(Comment, resp.get("data") if resp else None)

    def delete(self, file_id: str, comment_id: str) -> None:
        """Delete a comment."""
        self._http.request_json("DELETE", f"/files/{file_id}/comments/{comment_id}")

    def get_replies(self, file_id: str, comment_id: str) -> List[Comment]:
        """Get replies to a comment."""
        resp = self._http.request_json("GET", f"/files/{file_id}/comments/{comment_id}/replies")
        return _from_dict_list(Comment, resp.get("data", []) if resp else [])


class AsyncCommentsService:
    """Asynchronous file comment operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def create(self, file_id: str, request: CreateCommentRequest) -> Comment:
        resp = await self._http.request_json("POST", f"/files/{file_id}/comments", body=request)
        return _from_dict(Comment, resp.get("data") if resp else None)

    async def list(self, file_id: str) -> List[Comment]:
        resp = await self._http.request_json("GET", f"/files/{file_id}/comments")
        return _from_dict_list(Comment, resp.get("data", []) if resp else [])

    async def get(self, file_id: str, comment_id: str) -> Comment:
        resp = await self._http.request_json("GET", f"/files/{file_id}/comments/{comment_id}")
        return _from_dict(Comment, resp.get("data") if resp else None)

    async def update(self, file_id: str, comment_id: str, request: UpdateCommentRequest) -> Comment:
        resp = await self._http.request_json("PATCH", f"/files/{file_id}/comments/{comment_id}", body=request)
        return _from_dict(Comment, resp.get("data") if resp else None)

    async def delete(self, file_id: str, comment_id: str) -> None:
        await self._http.request_json("DELETE", f"/files/{file_id}/comments/{comment_id}")

    async def get_replies(self, file_id: str, comment_id: str) -> List[Comment]:
        resp = await self._http.request_json("GET", f"/files/{file_id}/comments/{comment_id}/replies")
        return _from_dict_list(Comment, resp.get("data", []) if resp else [])
