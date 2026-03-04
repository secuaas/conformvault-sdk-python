"""Activity subscriptions service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import List

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import ActivitySubscription, CreateActivitySubscriptionRequest


class ActivitySubscriptionsService:
    """Synchronous activity subscription operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def subscribe(self, request: CreateActivitySubscriptionRequest) -> ActivitySubscription:
        """Create an activity subscription."""
        resp = self._http.request_json("POST", "/activity/subscriptions", body=request)
        return _from_dict(ActivitySubscription, resp.get("data") if resp else None)

    def list(self) -> List[ActivitySubscription]:
        """List all activity subscriptions."""
        resp = self._http.request_json("GET", "/activity/subscriptions")
        return _from_dict_list(ActivitySubscription, resp.get("data", []) if resp else [])

    def unsubscribe(self, subscription_id: str) -> None:
        """Delete an activity subscription."""
        self._http.request_json("DELETE", f"/activity/subscriptions/{subscription_id}")


class AsyncActivitySubscriptionsService:
    """Asynchronous activity subscription operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def subscribe(self, request: CreateActivitySubscriptionRequest) -> ActivitySubscription:
        resp = await self._http.request_json("POST", "/activity/subscriptions", body=request)
        return _from_dict(ActivitySubscription, resp.get("data") if resp else None)

    async def list(self) -> List[ActivitySubscription]:
        resp = await self._http.request_json("GET", "/activity/subscriptions")
        return _from_dict_list(ActivitySubscription, resp.get("data", []) if resp else [])

    async def unsubscribe(self, subscription_id: str) -> None:
        await self._http.request_json("DELETE", f"/activity/subscriptions/{subscription_id}")
