"""Audit service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import AuditAnomaly, AuditEntry, AuditStats


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

    def search(
        self,
        *,
        query: Optional[str] = None,
        event_type: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: int = 0,
        limit: int = 0,
    ) -> List[AuditEntry]:
        """Search audit log entries.

        Args:
            query: Free-text search query.
            event_type: Filter by event type.
            from_date: Start date filter (ISO 8601 string).
            to_date: End date filter (ISO 8601 string).
            page: Page number (1-based).
            limit: Maximum entries per page.
        """
        params: Dict[str, Any] = {}
        if query:
            params["q"] = query
        if event_type:
            params["event_type"] = event_type
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit
        resp = self._http.request_json("GET", "/audit/search", params=params or None)
        return _from_dict_list(AuditEntry, resp.get("data", []) if resp else [])

    def export(
        self,
        *,
        format: Optional[str] = None,
        event_type: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Any:
        """Export audit logs as a streaming response.

        Args:
            format: Export format (e.g. ``"csv"``, ``"json"``).
            event_type: Filter by event type.
            from_date: Start date filter (ISO 8601 string).
            to_date: End date filter (ISO 8601 string).

        Returns:
            A streaming ``httpx.Response``.  The caller is responsible for
            reading and closing it.
        """
        params: Dict[str, str] = {}
        if format:
            params["format"] = format
        if event_type:
            params["event_type"] = event_type
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        path = "/audit/export"
        if params:
            path = f"{path}?{urlencode(params)}"
        return self._http.request_stream("GET", path)

    def get_stats(self) -> AuditStats:
        """Get audit log statistics."""
        resp = self._http.request_json("GET", "/audit/stats")
        return _from_dict(AuditStats, resp.get("data") if resp else None)

    def get_anomalies(self) -> List[AuditAnomaly]:
        """Get detected audit anomalies."""
        resp = self._http.request_json("GET", "/audit/anomalies")
        return _from_dict_list(AuditAnomaly, resp.get("data", []) if resp else [])


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

    async def search(
        self,
        *,
        query: Optional[str] = None,
        event_type: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: int = 0,
        limit: int = 0,
    ) -> List[AuditEntry]:
        params: Dict[str, Any] = {}
        if query:
            params["q"] = query
        if event_type:
            params["event_type"] = event_type
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit
        resp = await self._http.request_json("GET", "/audit/search", params=params or None)
        return _from_dict_list(AuditEntry, resp.get("data", []) if resp else [])

    async def export(
        self,
        *,
        format: Optional[str] = None,
        event_type: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Any:
        params: Dict[str, str] = {}
        if format:
            params["format"] = format
        if event_type:
            params["event_type"] = event_type
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        path = "/audit/export"
        if params:
            path = f"{path}?{urlencode(params)}"
        return await self._http.request_stream("GET", path)

    async def get_stats(self) -> AuditStats:
        resp = await self._http.request_json("GET", "/audit/stats")
        return _from_dict(AuditStats, resp.get("data") if resp else None)

    async def get_anomalies(self) -> List[AuditAnomaly]:
        resp = await self._http.request_json("GET", "/audit/anomalies")
        return _from_dict_list(AuditAnomaly, resp.get("data", []) if resp else [])
