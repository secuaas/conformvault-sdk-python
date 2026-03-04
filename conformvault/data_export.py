"""Data export service for the ConformVault Python SDK."""

from __future__ import annotations

from .client import _AsyncHTTP, _SyncHTTP, _from_dict
from .types import UserDataExport


class DataExportService:
    """Synchronous user data export operations (GDPR/Loi 25)."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def export(self, user_id: str) -> UserDataExport:
        """Request a data export for a user."""
        resp = self._http.request_json("GET", f"/users/{user_id}/export")
        return _from_dict(UserDataExport, resp.get("data") if resp else None)


class AsyncDataExportService:
    """Asynchronous user data export operations (GDPR/Loi 25)."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def export(self, user_id: str) -> UserDataExport:
        resp = await self._http.request_json("GET", f"/users/{user_id}/export")
        return _from_dict(UserDataExport, resp.get("data") if resp else None)
