"""Batch operation endpoints for the ConformVault API."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import BatchOperation


class BatchesService:
    """Synchronous batch operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def create(
        self,
        batch_type: str,
        items: List[Dict[str, Any]],
        *,
        folder_id: Optional[str] = None,
    ) -> BatchOperation:
        """Create a new batch operation."""
        body: Dict[str, Any] = {"type": batch_type, "items": items}
        if folder_id is not None:
            body["folder_id"] = folder_id
        resp = self._http.request_json("POST", "/batches", body=body)
        return _from_dict(BatchOperation, resp.get("data") if resp else None)

    def list(self, *, page: int = 0, limit: int = 0) -> List[BatchOperation]:
        """List batch operations with optional pagination."""
        params: Dict[str, str] = {}
        if page > 0:
            params["page"] = str(page)
        if limit > 0:
            params["limit"] = str(limit)
        resp = self._http.request_json("GET", "/batches", params=params or None)
        return _from_dict_list(BatchOperation, resp.get("data", []) if resp else [])

    def get(self, batch_id: str) -> BatchOperation:
        """Get a single batch operation by ID."""
        resp = self._http.request_json("GET", f"/batches/{batch_id}")
        return _from_dict(BatchOperation, resp.get("data") if resp else None)

    def commit(self, batch_id: str) -> BatchOperation:
        """Commit a batch operation to trigger processing."""
        resp = self._http.request_json("POST", f"/batches/{batch_id}/commit")
        return _from_dict(BatchOperation, resp.get("data") if resp else None)

    def cancel(self, batch_id: str) -> None:
        """Cancel a batch operation."""
        self._http.request_json("POST", f"/batches/{batch_id}/cancel")


class AsyncBatchesService:
    """Asynchronous batch operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def create(
        self,
        batch_type: str,
        items: List[Dict[str, Any]],
        *,
        folder_id: Optional[str] = None,
    ) -> BatchOperation:
        body: Dict[str, Any] = {"type": batch_type, "items": items}
        if folder_id is not None:
            body["folder_id"] = folder_id
        resp = await self._http.request_json("POST", "/batches", body=body)
        return _from_dict(BatchOperation, resp.get("data") if resp else None)

    async def list(self, *, page: int = 0, limit: int = 0) -> List[BatchOperation]:
        params: Dict[str, str] = {}
        if page > 0:
            params["page"] = str(page)
        if limit > 0:
            params["limit"] = str(limit)
        resp = await self._http.request_json("GET", "/batches", params=params or None)
        return _from_dict_list(BatchOperation, resp.get("data", []) if resp else [])

    async def get(self, batch_id: str) -> BatchOperation:
        resp = await self._http.request_json("GET", f"/batches/{batch_id}")
        return _from_dict(BatchOperation, resp.get("data") if resp else None)

    async def commit(self, batch_id: str) -> BatchOperation:
        resp = await self._http.request_json("POST", f"/batches/{batch_id}/commit")
        return _from_dict(BatchOperation, resp.get("data") if resp else None)

    async def cancel(self, batch_id: str) -> None:
        await self._http.request_json("POST", f"/batches/{batch_id}/cancel")
