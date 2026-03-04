"""Jobs service for the ConformVault Python SDK."""

from __future__ import annotations

from typing import List

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import CreateJobRequest, Job


class JobsService:
    """Synchronous background job operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def create(self, request: CreateJobRequest) -> Job:
        """Create a background job."""
        resp = self._http.request_json("POST", "/jobs", body=request)
        return _from_dict(Job, resp.get("data") if resp else None)

    def list(self) -> List[Job]:
        """List all jobs."""
        resp = self._http.request_json("GET", "/jobs")
        return _from_dict_list(Job, resp.get("data", []) if resp else [])

    def get(self, job_id: str) -> Job:
        """Get a job by ID."""
        resp = self._http.request_json("GET", f"/jobs/{job_id}")
        return _from_dict(Job, resp.get("data") if resp else None)

    def cancel(self, job_id: str) -> None:
        """Cancel a running job."""
        self._http.request_json("POST", f"/jobs/{job_id}/cancel")


class AsyncJobsService:
    """Asynchronous background job operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def create(self, request: CreateJobRequest) -> Job:
        resp = await self._http.request_json("POST", "/jobs", body=request)
        return _from_dict(Job, resp.get("data") if resp else None)

    async def list(self) -> List[Job]:
        resp = await self._http.request_json("GET", "/jobs")
        return _from_dict_list(Job, resp.get("data", []) if resp else [])

    async def get(self, job_id: str) -> Job:
        resp = await self._http.request_json("GET", f"/jobs/{job_id}")
        return _from_dict(Job, resp.get("data") if resp else None)

    async def cancel(self, job_id: str) -> None:
        await self._http.request_json("POST", f"/jobs/{job_id}/cancel")
