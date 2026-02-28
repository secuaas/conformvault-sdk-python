"""Scan reports service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import Dict, List, Optional

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import FileScanReport, FileScanSummary


class ScanReportsService:
    """Synchronous ClamAV scan report operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def get_report(self, file_id: str) -> FileScanReport:
        """Get the scan report for a specific file.

        Args:
            file_id: The UUID of the file to retrieve the scan report for.
        """
        resp = self._http.request_json("GET", f"/files/{file_id}/scan-report")
        return _from_dict(FileScanReport, resp.get("data") if resp else None)

    def list(self, *, limit: int = 20, offset: int = 0) -> List[FileScanReport]:
        """List scan reports for the organization.

        Args:
            limit: Maximum number of reports to return.
            offset: Number of reports to skip (for pagination).
        """
        params: Dict[str, str] = {}
        if limit != 20:
            params["limit"] = str(limit)
        if offset > 0:
            params["offset"] = str(offset)

        resp = self._http.request_json("GET", "/scan-reports", params=params or None)
        return _from_dict_list(FileScanReport, resp.get("data", []) if resp else [])

    def get_summary(self) -> FileScanSummary:
        """Get a summary of scan statistics for the organization."""
        resp = self._http.request_json("GET", "/scan-reports/summary")
        return _from_dict(FileScanSummary, resp.get("data") if resp else None)


class AsyncScanReportsService:
    """Asynchronous ClamAV scan report operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def get_report(self, file_id: str) -> FileScanReport:
        resp = await self._http.request_json("GET", f"/files/{file_id}/scan-report")
        return _from_dict(FileScanReport, resp.get("data") if resp else None)

    async def list(self, *, limit: int = 20, offset: int = 0) -> List[FileScanReport]:
        params: Dict[str, str] = {}
        if limit != 20:
            params["limit"] = str(limit)
        if offset > 0:
            params["offset"] = str(offset)

        resp = await self._http.request_json("GET", "/scan-reports", params=params or None)
        return _from_dict_list(FileScanReport, resp.get("data", []) if resp else [])

    async def get_summary(self) -> FileScanSummary:
        resp = await self._http.request_json("GET", "/scan-reports/summary")
        return _from_dict(FileScanSummary, resp.get("data") if resp else None)
