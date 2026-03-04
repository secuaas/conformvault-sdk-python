"""Quota and rate limit services for the ConformVault Python SDK."""

from __future__ import annotations

from .client import _AsyncHTTP, _SyncHTTP, _from_dict
from .types import QuotaInfo, RateLimitInfo


class QuotaService:
    """Synchronous quota operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def get(self) -> QuotaInfo:
        """Get current quota usage."""
        resp = self._http.request_json("GET", "/quota")
        return _from_dict(QuotaInfo, resp.get("data") if resp else None)


class AsyncQuotaService:
    """Asynchronous quota operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def get(self) -> QuotaInfo:
        resp = await self._http.request_json("GET", "/quota")
        return _from_dict(QuotaInfo, resp.get("data") if resp else None)


class RateLimitService:
    """Synchronous rate limit operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def get(self) -> RateLimitInfo:
        """Get current rate limit status."""
        resp = self._http.request_json("GET", "/rate-limit")
        return _from_dict(RateLimitInfo, resp.get("data") if resp else None)


class AsyncRateLimitService:
    """Asynchronous rate limit operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def get(self) -> RateLimitInfo:
        resp = await self._http.request_json("GET", "/rate-limit")
        return _from_dict(RateLimitInfo, resp.get("data") if resp else None)
