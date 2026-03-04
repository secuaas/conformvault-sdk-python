"""Document template operations for the ConformVault API."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .client import _AsyncHTTP, _SyncHTTP, _from_dict, _from_dict_list
from .types import DocumentTemplate, GeneratedDocument


class TemplatesService:
    """Synchronous document template operations."""

    def __init__(self, http: _SyncHTTP) -> None:
        self._http = http

    def create(
        self,
        name: str,
        content_type: str,
        *,
        description: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ) -> DocumentTemplate:
        """Create a new document template."""
        body: Dict[str, Any] = {"name": name, "content_type": content_type}
        if description is not None:
            body["description"] = description
        if fields is not None:
            body["fields"] = fields
        resp = self._http.request_json("POST", "/templates", body=body)
        return _from_dict(DocumentTemplate, resp.get("data") if resp else None)

    def list(self, *, page: int = 0, limit: int = 0) -> List[DocumentTemplate]:
        """List document templates with optional pagination."""
        params: Dict[str, str] = {}
        if page > 0:
            params["page"] = str(page)
        if limit > 0:
            params["limit"] = str(limit)
        resp = self._http.request_json("GET", "/templates", params=params or None)
        return _from_dict_list(DocumentTemplate, resp.get("data", []) if resp else [])

    def get(self, template_id: str) -> DocumentTemplate:
        """Get a single document template by ID."""
        resp = self._http.request_json("GET", f"/templates/{template_id}")
        return _from_dict(DocumentTemplate, resp.get("data") if resp else None)

    def update(
        self,
        template_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ) -> DocumentTemplate:
        """Update a document template."""
        body: Dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if fields is not None:
            body["fields"] = fields
        resp = self._http.request_json("PUT", f"/templates/{template_id}", body=body)
        return _from_dict(DocumentTemplate, resp.get("data") if resp else None)

    def delete(self, template_id: str) -> None:
        """Delete a document template."""
        self._http.request_json("DELETE", f"/templates/{template_id}")

    def generate(self, template_id: str, data: Dict[str, str], *, filename: Optional[str] = None) -> bytes:
        """Generate a PDF document from a template and return its bytes."""
        body: Dict[str, Any] = {"data": data}
        if filename is not None:
            body["filename"] = filename
        resp = self._http.request_stream_with_body("POST", f"/templates/{template_id}/generate", body=body)
        try:
            return resp.read()
        finally:
            resp.close()

    def list_documents(self, template_id: str) -> List[GeneratedDocument]:
        """List documents generated from a template."""
        resp = self._http.request_json("GET", f"/templates/{template_id}/documents")
        return _from_dict_list(GeneratedDocument, resp.get("data", []) if resp else [])


class AsyncTemplatesService:
    """Asynchronous document template operations."""

    def __init__(self, http: _AsyncHTTP) -> None:
        self._http = http

    async def create(
        self,
        name: str,
        content_type: str,
        *,
        description: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ) -> DocumentTemplate:
        body: Dict[str, Any] = {"name": name, "content_type": content_type}
        if description is not None:
            body["description"] = description
        if fields is not None:
            body["fields"] = fields
        resp = await self._http.request_json("POST", "/templates", body=body)
        return _from_dict(DocumentTemplate, resp.get("data") if resp else None)

    async def list(self, *, page: int = 0, limit: int = 0) -> List[DocumentTemplate]:
        params: Dict[str, str] = {}
        if page > 0:
            params["page"] = str(page)
        if limit > 0:
            params["limit"] = str(limit)
        resp = await self._http.request_json("GET", "/templates", params=params or None)
        return _from_dict_list(DocumentTemplate, resp.get("data", []) if resp else [])

    async def get(self, template_id: str) -> DocumentTemplate:
        resp = await self._http.request_json("GET", f"/templates/{template_id}")
        return _from_dict(DocumentTemplate, resp.get("data") if resp else None)

    async def update(
        self,
        template_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ) -> DocumentTemplate:
        body: Dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if fields is not None:
            body["fields"] = fields
        resp = await self._http.request_json("PUT", f"/templates/{template_id}", body=body)
        return _from_dict(DocumentTemplate, resp.get("data") if resp else None)

    async def delete(self, template_id: str) -> None:
        await self._http.request_json("DELETE", f"/templates/{template_id}")

    async def generate(self, template_id: str, data: Dict[str, str], *, filename: Optional[str] = None) -> bytes:
        """Generate a PDF document from a template and return its bytes."""
        body: Dict[str, Any] = {"data": data}
        if filename is not None:
            body["filename"] = filename
        resp = await self._http.request_stream_with_body("POST", f"/templates/{template_id}/generate", body=body)
        try:
            return await resp.aread()
        finally:
            await resp.aclose()

    async def list_documents(self, template_id: str) -> List[GeneratedDocument]:
        resp = await self._http.request_json("GET", f"/templates/{template_id}/documents")
        return _from_dict_list(GeneratedDocument, resp.get("data", []) if resp else [])
