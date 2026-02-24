"""API keys service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import List

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import APIKey, CreateAPIKeyRequest, CreateAPIKeyResponse


class KeysService:
    """Synchronous API key self-management."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def list(self) -> List[APIKey]:
        """List all API keys for the organization."""
        resp = self._http.request_json("GET", "/keys")
        return _from_dict_list(APIKey, resp.get("data", []) if resp else [])

    def create(self, request: CreateAPIKeyRequest) -> CreateAPIKeyResponse:
        """Create a new API key. The full key is returned once."""
        resp = self._http.request_json("POST", "/keys", body=request)
        return _from_dict(CreateAPIKeyResponse, resp.get("data") if resp else None)

    def get(self, key_id: str) -> APIKey:
        """Get a single API key by ID."""
        resp = self._http.request_json("GET", f"/keys/{key_id}")
        return _from_dict(APIKey, resp.get("data") if resp else None)

    def revoke(self, key_id: str) -> None:
        """Revoke (delete) an API key."""
        self._http.request_json("DELETE", f"/keys/{key_id}")

    def rotate(self, key_id: str) -> CreateAPIKeyResponse:
        """Rotate an API key, returning the new key value."""
        resp = self._http.request_json("POST", f"/keys/{key_id}/rotate")
        return _from_dict(CreateAPIKeyResponse, resp.get("data") if resp else None)


class AsyncKeysService:
    """Asynchronous API key self-management."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def list(self) -> List[APIKey]:
        resp = await self._http.request_json("GET", "/keys")
        return _from_dict_list(APIKey, resp.get("data", []) if resp else [])

    async def create(self, request: CreateAPIKeyRequest) -> CreateAPIKeyResponse:
        resp = await self._http.request_json("POST", "/keys", body=request)
        return _from_dict(CreateAPIKeyResponse, resp.get("data") if resp else None)

    async def get(self, key_id: str) -> APIKey:
        resp = await self._http.request_json("GET", f"/keys/{key_id}")
        return _from_dict(APIKey, resp.get("data") if resp else None)

    async def revoke(self, key_id: str) -> None:
        await self._http.request_json("DELETE", f"/keys/{key_id}")

    async def rotate(self, key_id: str) -> CreateAPIKeyResponse:
        resp = await self._http.request_json("POST", f"/keys/{key_id}/rotate")
        return _from_dict(CreateAPIKeyResponse, resp.get("data") if resp else None)
