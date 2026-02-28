"""Bulk file operations service."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .client import _AsyncHTTP, _SyncHTTP


@dataclass
class BulkError:
    file_id: str = ""
    error: str = ""


@dataclass
class BulkResult:
    processed: int = 0
    succeeded: int = 0
    failed: int = 0
    errors: List[BulkError] = field(default_factory=list)


class BulkService:
    """Synchronous bulk file operations."""

    def __init__(self, http: "_SyncHTTP") -> None:
        self._http = http

    def delete(self, file_ids: List[str]) -> BulkResult:
        """Soft-delete multiple files at once."""
        data = self._http.request_json("POST", "/files/bulk-delete", body={"file_ids": file_ids})
        return BulkResult(
            processed=data.get("processed", 0),
            succeeded=data.get("succeeded", 0),
            failed=data.get("failed", 0),
            errors=[BulkError(**e) for e in data.get("errors", [])],
        )

    def move(self, file_ids: List[str], target_folder_id: str) -> BulkResult:
        """Move multiple files to a target folder."""
        data = self._http.request_json(
            "POST", "/files/bulk-move",
            body={"file_ids": file_ids, "target_folder_id": target_folder_id},
        )
        return BulkResult(
            processed=data.get("processed", 0),
            succeeded=data.get("succeeded", 0),
            failed=data.get("failed", 0),
            errors=[BulkError(**e) for e in data.get("errors", [])],
        )

    def download(self, file_ids: List[str]):
        """Download multiple files as a ZIP archive. Returns a streaming response."""
        return self._http.request_json("POST", "/files/bulk-download", body={"file_ids": file_ids})


class AsyncBulkService:
    """Asynchronous bulk file operations."""

    def __init__(self, http: "_AsyncHTTP") -> None:
        self._http = http

    async def delete(self, file_ids: List[str]) -> BulkResult:
        data = await self._http.request_json("POST", "/files/bulk-delete", body={"file_ids": file_ids})
        return BulkResult(
            processed=data.get("processed", 0),
            succeeded=data.get("succeeded", 0),
            failed=data.get("failed", 0),
            errors=[BulkError(**e) for e in data.get("errors", [])],
        )

    async def move(self, file_ids: List[str], target_folder_id: str) -> BulkResult:
        data = await self._http.request_json(
            "POST", "/files/bulk-move",
            body={"file_ids": file_ids, "target_folder_id": target_folder_id},
        )
        return BulkResult(
            processed=data.get("processed", 0),
            succeeded=data.get("succeeded", 0),
            failed=data.get("failed", 0),
            errors=[BulkError(**e) for e in data.get("errors", [])],
        )

    async def download(self, file_ids: List[str]):
        return await self._http.request_json("POST", "/files/bulk-download", body={"file_ids": file_ids})
