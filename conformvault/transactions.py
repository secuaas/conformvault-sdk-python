"""Transaction folder operations for the ConformVault API."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import TransactionFolder, TransactionFolderItem


class TransactionsService:
    """Synchronous transaction folder operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def create(
        self,
        name: str,
        *,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> TransactionFolder:
        """Create a new transaction folder."""
        body: Dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        if due_date is not None:
            body["due_date"] = due_date
        resp = self._http.request_json("POST", "/transactions", body=body)
        return _from_dict(TransactionFolder, resp.get("data") if resp else None)

    def list(self, *, page: int = 0, limit: int = 0) -> List[TransactionFolder]:
        """List transaction folders with optional pagination."""
        params: Dict[str, str] = {}
        if page > 0:
            params["page"] = str(page)
        if limit > 0:
            params["limit"] = str(limit)
        resp = self._http.request_json("GET", "/transactions", params=params or None)
        return _from_dict_list(TransactionFolder, resp.get("data", []) if resp else [])

    def get(self, transaction_id: str) -> TransactionFolder:
        """Get a single transaction folder by ID."""
        resp = self._http.request_json("GET", f"/transactions/{transaction_id}")
        return _from_dict(TransactionFolder, resp.get("data") if resp else None)

    def update(
        self,
        transaction_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> TransactionFolder:
        """Update a transaction folder."""
        body: Dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if status is not None:
            body["status"] = status
        if due_date is not None:
            body["due_date"] = due_date
        resp = self._http.request_json("PUT", f"/transactions/{transaction_id}", body=body)
        return _from_dict(TransactionFolder, resp.get("data") if resp else None)

    def delete(self, transaction_id: str) -> None:
        """Delete a transaction folder."""
        self._http.request_json("DELETE", f"/transactions/{transaction_id}")

    def add_item(
        self,
        transaction_id: str,
        label: str,
        *,
        description: Optional[str] = None,
        required: Optional[bool] = None,
    ) -> TransactionFolderItem:
        """Add an item to a transaction folder."""
        body: Dict[str, Any] = {"label": label}
        if description is not None:
            body["description"] = description
        if required is not None:
            body["required"] = required
        resp = self._http.request_json("POST", f"/transactions/{transaction_id}/items", body=body)
        return _from_dict(TransactionFolderItem, resp.get("data") if resp else None)

    def update_item(
        self,
        transaction_id: str,
        item_id: str,
        *,
        label: Optional[str] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        status: Optional[str] = None,
        file_id: Optional[str] = None,
    ) -> TransactionFolderItem:
        """Update an item in a transaction folder."""
        body: Dict[str, Any] = {}
        if label is not None:
            body["label"] = label
        if description is not None:
            body["description"] = description
        if required is not None:
            body["required"] = required
        if status is not None:
            body["status"] = status
        if file_id is not None:
            body["file_id"] = file_id
        resp = self._http.request_json("PUT", f"/transactions/{transaction_id}/items/{item_id}", body=body)
        return _from_dict(TransactionFolderItem, resp.get("data") if resp else None)

    def delete_item(self, transaction_id: str, item_id: str) -> None:
        """Delete an item from a transaction folder."""
        self._http.request_json("DELETE", f"/transactions/{transaction_id}/items/{item_id}")


class AsyncTransactionsService:
    """Asynchronous transaction folder operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def create(
        self,
        name: str,
        *,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> TransactionFolder:
        body: Dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        if due_date is not None:
            body["due_date"] = due_date
        resp = await self._http.request_json("POST", "/transactions", body=body)
        return _from_dict(TransactionFolder, resp.get("data") if resp else None)

    async def list(self, *, page: int = 0, limit: int = 0) -> List[TransactionFolder]:
        params: Dict[str, str] = {}
        if page > 0:
            params["page"] = str(page)
        if limit > 0:
            params["limit"] = str(limit)
        resp = await self._http.request_json("GET", "/transactions", params=params or None)
        return _from_dict_list(TransactionFolder, resp.get("data", []) if resp else [])

    async def get(self, transaction_id: str) -> TransactionFolder:
        resp = await self._http.request_json("GET", f"/transactions/{transaction_id}")
        return _from_dict(TransactionFolder, resp.get("data") if resp else None)

    async def update(
        self,
        transaction_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> TransactionFolder:
        body: Dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if status is not None:
            body["status"] = status
        if due_date is not None:
            body["due_date"] = due_date
        resp = await self._http.request_json("PUT", f"/transactions/{transaction_id}", body=body)
        return _from_dict(TransactionFolder, resp.get("data") if resp else None)

    async def delete(self, transaction_id: str) -> None:
        await self._http.request_json("DELETE", f"/transactions/{transaction_id}")

    async def add_item(
        self,
        transaction_id: str,
        label: str,
        *,
        description: Optional[str] = None,
        required: Optional[bool] = None,
    ) -> TransactionFolderItem:
        body: Dict[str, Any] = {"label": label}
        if description is not None:
            body["description"] = description
        if required is not None:
            body["required"] = required
        resp = await self._http.request_json("POST", f"/transactions/{transaction_id}/items", body=body)
        return _from_dict(TransactionFolderItem, resp.get("data") if resp else None)

    async def update_item(
        self,
        transaction_id: str,
        item_id: str,
        *,
        label: Optional[str] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        status: Optional[str] = None,
        file_id: Optional[str] = None,
    ) -> TransactionFolderItem:
        body: Dict[str, Any] = {}
        if label is not None:
            body["label"] = label
        if description is not None:
            body["description"] = description
        if required is not None:
            body["required"] = required
        if status is not None:
            body["status"] = status
        if file_id is not None:
            body["file_id"] = file_id
        resp = await self._http.request_json("PUT", f"/transactions/{transaction_id}/items/{item_id}", body=body)
        return _from_dict(TransactionFolderItem, resp.get("data") if resp else None)

    async def delete_item(self, transaction_id: str, item_id: str) -> None:
        await self._http.request_json("DELETE", f"/transactions/{transaction_id}/items/{item_id}")
