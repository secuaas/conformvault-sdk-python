"""Audit service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import Dict, List, Optional

from .client import _AsyncHTTP, _SyncHTTP, _from_dict_list
from .types import AuditEntry


class AuditService:
    """Synchronous audit log operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def list(
        self,
        *,
        event_type: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: int = 0,
        limit: int = 0,
    ) -> List[AuditEntry]:
        """List audit log entries with optional filters.

        Args:
            event_type: Filter by event type (e.g. ``"file.uploaded"``).
            from_date: Start date filter (ISO 8601 string).
            to_date: End date filter (ISO 8601 string).
            page: Page number (1-based).
            limit: Maximum entries per page.
        """
        params: Dict[str, str] = {}
        if event_type:
            params["event_type"] = event_type
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if page > 0:
            params["page"] = str(page)
        if limit > 0:
            params["limit"] = str(limit)

        resp = self._http.request_json("GET", "/audit", params=params or None)
        return _from_dict_list(AuditEntry, resp.get("data", []) if resp else [])


class AsyncAuditService:
    """Asynchronous audit log operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def list(
        self,
        *,
        event_type: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: int = 0,
        limit: int = 0,
    ) -> List[AuditEntry]:
        params: Dict[str, str] = {}
        if event_type:
            params["event_type"] = event_type
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if page > 0:
            params["page"] = str(page)
        if limit > 0:
            params["limit"] = str(limit)

        resp = await self._http.request_json("GET", "/audit", params=params or None)
        return _from_dict_list(AuditEntry, resp.get("data", []) if resp else [])
