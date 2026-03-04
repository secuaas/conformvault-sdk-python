"""Policies service for the ConformVault Python SDK."""

from __future__ import annotations

from .client import _AsyncHTTP, _SyncHTTP, _from_dict
from .types import (
    EncryptionSalt,
    IPPolicy,
    MFAPolicy,
    SetEncryptionSaltRequest,
    SetIPPolicyRequest,
    SetMFAPolicyRequest,
)


class PoliciesService:
    """Synchronous policy operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def get_ip_policy(self) -> IPPolicy:
        """Get the IP access policy."""
        resp = self._http.request_json("GET", "/ip-policy")
        return _from_dict(IPPolicy, resp.get("data") if resp else None)

    def set_ip_policy(self, request: SetIPPolicyRequest) -> IPPolicy:
        """Set the IP access policy."""
        resp = self._http.request_json("PUT", "/ip-policy", body=request)
        return _from_dict(IPPolicy, resp.get("data") if resp else None)

    def get_mfa_policy(self) -> MFAPolicy:
        """Get the MFA policy."""
        resp = self._http.request_json("GET", "/mfa-policy")
        return _from_dict(MFAPolicy, resp.get("data") if resp else None)

    def set_mfa_policy(self, request: SetMFAPolicyRequest) -> MFAPolicy:
        """Set the MFA policy."""
        resp = self._http.request_json("PUT", "/mfa-policy", body=request)
        return _from_dict(MFAPolicy, resp.get("data") if resp else None)

    def get_encryption_salt(self) -> EncryptionSalt:
        """Get the encryption salt."""
        resp = self._http.request_json("GET", "/encryption/salt")
        return _from_dict(EncryptionSalt, resp.get("data") if resp else None)

    def set_encryption_salt(self, request: SetEncryptionSaltRequest) -> EncryptionSalt:
        """Set the encryption salt."""
        resp = self._http.request_json("PUT", "/encryption/salt", body=request)
        return _from_dict(EncryptionSalt, resp.get("data") if resp else None)


class AsyncPoliciesService:
    """Asynchronous policy operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def get_ip_policy(self) -> IPPolicy:
        resp = await self._http.request_json("GET", "/ip-policy")
        return _from_dict(IPPolicy, resp.get("data") if resp else None)

    async def set_ip_policy(self, request: SetIPPolicyRequest) -> IPPolicy:
        resp = await self._http.request_json("PUT", "/ip-policy", body=request)
        return _from_dict(IPPolicy, resp.get("data") if resp else None)

    async def get_mfa_policy(self) -> MFAPolicy:
        resp = await self._http.request_json("GET", "/mfa-policy")
        return _from_dict(MFAPolicy, resp.get("data") if resp else None)

    async def set_mfa_policy(self, request: SetMFAPolicyRequest) -> MFAPolicy:
        resp = await self._http.request_json("PUT", "/mfa-policy", body=request)
        return _from_dict(MFAPolicy, resp.get("data") if resp else None)

    async def get_encryption_salt(self) -> EncryptionSalt:
        resp = await self._http.request_json("GET", "/encryption/salt")
        return _from_dict(EncryptionSalt, resp.get("data") if resp else None)

    async def set_encryption_salt(self, request: SetEncryptionSaltRequest) -> EncryptionSalt:
        resp = await self._http.request_json("PUT", "/encryption/salt", body=request)
        return _from_dict(EncryptionSalt, resp.get("data") if resp else None)
