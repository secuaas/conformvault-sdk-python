"""Retention policy service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import List

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import CreateRetentionPolicyRequest, RetentionPolicy, UpdateRetentionPolicyRequest


class RetentionService:
    """Synchronous retention policy operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def create(self, request: CreateRetentionPolicyRequest) -> RetentionPolicy:
        """Create a retention policy."""
        resp = self._http.request_json("POST", "/retention-policies", body=request)
        return _from_dict(RetentionPolicy, resp.get("data") if resp else None)

    def list(self) -> List[RetentionPolicy]:
        """List all retention policies."""
        resp = self._http.request_json("GET", "/retention-policies")
        return _from_dict_list(RetentionPolicy, resp.get("data", []) if resp else [])

    def get(self, policy_id: str) -> RetentionPolicy:
        """Get a retention policy by ID."""
        resp = self._http.request_json("GET", f"/retention-policies/{policy_id}")
        return _from_dict(RetentionPolicy, resp.get("data") if resp else None)

    def update(self, policy_id: str, request: UpdateRetentionPolicyRequest) -> RetentionPolicy:
        """Update a retention policy."""
        resp = self._http.request_json("PUT", f"/retention-policies/{policy_id}", body=request)
        return _from_dict(RetentionPolicy, resp.get("data") if resp else None)

    def delete(self, policy_id: str) -> None:
        """Delete a retention policy."""
        self._http.request_json("DELETE", f"/retention-policies/{policy_id}")


class AsyncRetentionService:
    """Asynchronous retention policy operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def create(self, request: CreateRetentionPolicyRequest) -> RetentionPolicy:
        resp = await self._http.request_json("POST", "/retention-policies", body=request)
        return _from_dict(RetentionPolicy, resp.get("data") if resp else None)

    async def list(self) -> List[RetentionPolicy]:
        resp = await self._http.request_json("GET", "/retention-policies")
        return _from_dict_list(RetentionPolicy, resp.get("data", []) if resp else [])

    async def get(self, policy_id: str) -> RetentionPolicy:
        resp = await self._http.request_json("GET", f"/retention-policies/{policy_id}")
        return _from_dict(RetentionPolicy, resp.get("data") if resp else None)

    async def update(self, policy_id: str, request: UpdateRetentionPolicyRequest) -> RetentionPolicy:
        resp = await self._http.request_json("PUT", f"/retention-policies/{policy_id}", body=request)
        return _from_dict(RetentionPolicy, resp.get("data") if resp else None)

    async def delete(self, policy_id: str) -> None:
        await self._http.request_json("DELETE", f"/retention-policies/{policy_id}")
