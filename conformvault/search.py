"""Unified search service."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional

from .client import _from_dict_list
from .types import SearchResult, SearchPagination

if TYPE_CHECKING:
    from .client import _AsyncHTTP, _SyncHTTP


class SearchService:
    """Synchronous search operations."""

    def __init__(self, http: "_SyncHTTP") -> None:
        self._http = http

    def search(
        self,
        query: str,
        *,
        types: Optional[str] = None,
        folder_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict:
        """Search across files and folders.

        Args:
            query: Search query string.
            types: Resource types to search ("files", "folders", or "files,folders").
            folder_id: Limit search to a specific folder.
            page: Page number (1-based).
            page_size: Results per page.

        Returns:
            Dict with "data" (list of SearchResult) and "pagination".
        """
        params: Dict[str, str] = {"q": query, "page": str(page), "page_size": str(page_size)}
        if types:
            params["types"] = types
        if folder_id:
            params["folder_id"] = folder_id

        data = self._http.request_json("GET", "/search", params=params)
        return {
            "data": _from_dict_list(SearchResult, data.get("data", []) if data else []),
            "pagination": data.get("pagination", {}) if data else {},
        }


class AsyncSearchService:
    """Asynchronous search operations."""

    def __init__(self, http: "_AsyncHTTP") -> None:
        self._http = http

    async def search(
        self,
        query: str,
        *,
        types: Optional[str] = None,
        folder_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict:
        params: Dict[str, str] = {"q": query, "page": str(page), "page_size": str(page_size)}
        if types:
            params["types"] = types
        if folder_id:
            params["folder_id"] = folder_id

        data = await self._http.request_json("GET", "/search", params=params)
        return {
            "data": _from_dict_list(SearchResult, data.get("data", []) if data else []),
            "pagination": data.get("pagination", {}) if data else {},
        }
