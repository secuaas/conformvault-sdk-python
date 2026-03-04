"""Bandwidth analytics service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import List

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import BandwidthSummary, DailyBandwidthStats


class BandwidthService:
    """Synchronous bandwidth analytics operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def get_summary(self) -> BandwidthSummary:
        """Get bandwidth usage summary."""
        resp = self._http.request_json("GET", "/bandwidth")
        return _from_dict(BandwidthSummary, resp.get("data") if resp else None)

    def get_daily(self) -> List[DailyBandwidthStats]:
        """Get daily bandwidth statistics."""
        resp = self._http.request_json("GET", "/bandwidth/daily")
        return _from_dict_list(DailyBandwidthStats, resp.get("data", []) if resp else [])


class AsyncBandwidthService:
    """Asynchronous bandwidth analytics operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def get_summary(self) -> BandwidthSummary:
        resp = await self._http.request_json("GET", "/bandwidth")
        return _from_dict(BandwidthSummary, resp.get("data") if resp else None)

    async def get_daily(self) -> List[DailyBandwidthStats]:
        resp = await self._http.request_json("GET", "/bandwidth/daily")
        return _from_dict_list(DailyBandwidthStats, resp.get("data", []) if resp else [])
