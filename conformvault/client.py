"""Sync and async HTTP clients for the ConformVault Developer API."""

from __future__ import annotations

import dataclasses
from typing import Any, BinaryIO, Dict, Optional, Type, TypeVar, Union

import httpx

from .errors import APIError, AuthenticationError, ConformVaultError, RateLimitError

DEFAULT_BASE_URL = "https://api.conformvault.com/dev/v1"
VERSION = "0.5.0"
USER_AGENT = f"conformvault-python/{VERSION}"

T = TypeVar("T")


def _build_headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": USER_AGENT,
    }


def _handle_error_response(response: httpx.Response) -> None:
    """Raise the appropriate exception for an error response."""
    status = response.status_code

    # Try to extract error message from JSON body
    message = ""
    try:
        body = response.json()
        message = body.get("error", "")
    except Exception:
        message = response.text or httpx.codes.get_reason_phrase(status)

    if not message:
        message = httpx.codes.get_reason_phrase(status)

    if status == 429:
        retry_after = 60.0
        ra = response.headers.get("Retry-After", "")
        if ra:
            try:
                retry_after = float(ra)
            except ValueError:
                pass
        raise RateLimitError(retry_after=retry_after, message=message)

    if status in (401, 403):
        raise AuthenticationError(message=message)

    raise APIError(status_code=status, message=message)


def _serialize_body(body: Any) -> Any:
    """Convert a dataclass (or dict) into a JSON-serialisable dict, dropping None values."""
    if body is None:
        return None
    if dataclasses.is_dataclass(body) and not isinstance(body, type):
        return _serialize_body(dataclasses.asdict(body))
    if isinstance(body, dict):
        cleaned: Dict[str, Any] = {}
        for k, v in body.items():
            if v is None:
                continue
            # Drop zero-value ints only for optional-feeling fields
            cleaned[k] = v
        return cleaned
    return body


def _from_dict(cls: Type[T], data: Any) -> T:
    """Instantiate a dataclass *cls* from a dict, ignoring unknown keys."""
    if data is None:
        return cls()  # type: ignore[call-arg]
    if not isinstance(data, dict):
        return data  # type: ignore[return-value]
    if not dataclasses.is_dataclass(cls):
        return data  # type: ignore[return-value]

    field_names = {f.name for f in dataclasses.fields(cls)}
    filtered = {k: v for k, v in data.items() if k in field_names}
    return cls(**filtered)


def _from_dict_list(cls: Type[T], items: Any) -> list[T]:
    """Convert a list of dicts into a list of dataclass instances."""
    if not isinstance(items, list):
        return []
    return [_from_dict(cls, item) for item in items]


# ---- Sync base client ----


class _SyncHTTP:
    """Low-level synchronous HTTP transport."""

    def __init__(self, api_key: str, base_url: str, timeout: float, http_client: Optional[httpx.Client]) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        if http_client is not None:
            self._client = http_client
        else:
            self._client = httpx.Client(
                timeout=timeout,
                headers=_build_headers(api_key),
            )

    # -- request helpers --

    def request_json(self, method: str, path: str, *, body: Any = None, params: Optional[Dict[str, str]] = None) -> Any:
        """Execute an HTTP request, return decoded JSON."""
        url = self._base_url + path
        kwargs: Dict[str, Any] = {"method": method, "url": url}
        if body is not None:
            kwargs["json"] = _serialize_body(body)
        if params:
            kwargs["params"] = params
        kwargs["headers"] = _build_headers(self._api_key)

        resp = self._client.request(**kwargs)
        if resp.status_code >= 400:
            _handle_error_response(resp)
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    def request_stream(self, method: str, path: str) -> httpx.Response:
        """Execute an HTTP request, return the raw streaming response.

        Caller is responsible for reading and closing the returned response.
        """
        url = self._base_url + path
        req = self._client.build_request(method, url, headers=_build_headers(self._api_key))
        resp = self._client.send(req, stream=True)
        if resp.status_code >= 400:
            resp.read()
            resp.close()
            _handle_error_response(resp)
        return resp

    def request_stream_with_body(self, method: str, path: str, body: Any = None) -> httpx.Response:
        """Execute request with a JSON body and return raw streaming response.

        Caller must close the response when done.
        """
        url = self._base_url + path
        headers = _build_headers(self._api_key)
        json_body = _serialize_body(body) if body is not None else None
        resp = self._client.send(
            self._client.build_request(method, url, json=json_body, headers=headers),
            stream=True,
        )
        if resp.status_code >= 400:
            resp.read()
            resp.close()
            _handle_error_response(resp)
        return resp

    def upload_file(
        self,
        path: str,
        file: Union[BinaryIO, bytes],
        filename: str,
        extra_fields: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Upload a file via multipart form-data."""
        url = self._base_url + path
        files_dict = {"file": (filename, file)}
        data = extra_fields or {}
        resp = self._client.post(
            url,
            files=files_dict,
            data=data,
            headers=_build_headers(self._api_key),
        )
        if resp.status_code >= 400:
            _handle_error_response(resp)
        return resp.json()

    def close(self) -> None:
        self._client.close()


# ---- Async base client ----


class _AsyncHTTP:
    """Low-level asynchronous HTTP transport."""

    def __init__(self, api_key: str, base_url: str, timeout: float, http_client: Optional[httpx.AsyncClient]) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        if http_client is not None:
            self._client = http_client
        else:
            self._client = httpx.AsyncClient(
                timeout=timeout,
                headers=_build_headers(api_key),
            )

    async def request_json(self, method: str, path: str, *, body: Any = None, params: Optional[Dict[str, str]] = None) -> Any:
        url = self._base_url + path
        kwargs: Dict[str, Any] = {"method": method, "url": url}
        if body is not None:
            kwargs["json"] = _serialize_body(body)
        if params:
            kwargs["params"] = params
        kwargs["headers"] = _build_headers(self._api_key)

        resp = await self._client.request(**kwargs)
        if resp.status_code >= 400:
            _handle_error_response(resp)
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    async def request_stream(self, method: str, path: str) -> httpx.Response:
        """Execute an async HTTP request, return the raw streaming response.

        Caller is responsible for reading and closing the returned response.
        """
        url = self._base_url + path
        req = self._client.build_request(method, url, headers=_build_headers(self._api_key))
        resp = await self._client.send(req, stream=True)
        if resp.status_code >= 400:
            await resp.aread()
            await resp.aclose()
            _handle_error_response(resp)
        return resp

    async def request_stream_with_body(self, method: str, path: str, body: Any = None) -> httpx.Response:
        """Execute async request with a JSON body and return raw streaming response.

        Caller must close the response when done.
        """
        url = self._base_url + path
        headers = _build_headers(self._api_key)
        json_body = _serialize_body(body) if body is not None else None
        resp = await self._client.send(
            self._client.build_request(method, url, json=json_body, headers=headers),
            stream=True,
        )
        if resp.status_code >= 400:
            await resp.aread()
            await resp.aclose()
            _handle_error_response(resp)
        return resp

    async def upload_file(
        self,
        path: str,
        file: Union[BinaryIO, bytes],
        filename: str,
        extra_fields: Optional[Dict[str, str]] = None,
    ) -> Any:
        url = self._base_url + path
        files_dict = {"file": (filename, file)}
        data = extra_fields or {}
        resp = await self._client.post(
            url,
            files=files_dict,
            data=data,
            headers=_build_headers(self._api_key),
        )
        if resp.status_code >= 400:
            _handle_error_response(resp)
        return resp.json()

    async def close(self) -> None:
        await self._client.aclose()


# ---- Public client classes ----

# Imports at the bottom to avoid circular dependencies.
from .files import AsyncFilesService, FilesService  # noqa: E402
from .folders import AsyncFoldersService, FoldersService  # noqa: E402
from .sharelinks import AsyncShareLinksService, ShareLinksService  # noqa: E402
from .signatures import AsyncSignaturesService, SignaturesService  # noqa: E402
from .webhooks import AsyncWebhooksService, WebhooksService  # noqa: E402
from .audit import AsyncAuditService, AuditService  # noqa: E402
from .keys import AsyncKeysService, KeysService  # noqa: E402
from .bulk import AsyncBulkService, BulkService  # noqa: E402
from .versions import AsyncVersionsService, VersionsService  # noqa: E402
from .search import AsyncSearchService, SearchService  # noqa: E402
from .trash import AsyncTrashService, TrashService  # noqa: E402
from .scan_reports import AsyncScanReportsService, ScanReportsService  # noqa: E402
from .attestation import AsyncAttestationService, AttestationService  # noqa: E402
from .transactions import AsyncTransactionsService, TransactionsService  # noqa: E402
from .templates import AsyncTemplatesService, TemplatesService  # noqa: E402
from .batches import AsyncBatchesService, BatchesService  # noqa: E402
from .metadata import AsyncMetadataService, MetadataService  # noqa: E402
from .retention import AsyncRetentionService, RetentionService  # noqa: E402
from .legal_holds import AsyncLegalHoldsService, LegalHoldsService  # noqa: E402
from .permissions import AsyncPermissionsService, PermissionsService  # noqa: E402
from .comments import AsyncCommentsService, CommentsService  # noqa: E402
from .quota import AsyncQuotaService, AsyncRateLimitService, QuotaService, RateLimitService  # noqa: E402
from .upload_sessions import AsyncUploadSessionsService, UploadSessionsService  # noqa: E402
from .jobs import AsyncJobsService, JobsService  # noqa: E402
from .activity_subscriptions import AsyncActivitySubscriptionsService, ActivitySubscriptionsService  # noqa: E402
from .policies import AsyncPoliciesService, PoliciesService  # noqa: E402


class ConformVault:
    """Synchronous client for the ConformVault Developer API.

    Usage::

        client = ConformVault("cvk_live_your_api_key")
        files = client.files.list()
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        self._http = _SyncHTTP(api_key, base_url, timeout, http_client)

        self.files = FilesService(self._http)
        self.folders = FoldersService(self._http)
        self.share_links = ShareLinksService(self._http)
        self.signatures = SignaturesService(self._http)
        self.webhooks = WebhooksService(self._http)
        self.audit = AuditService(self._http)
        self.keys = KeysService(self._http)
        self.bulk = BulkService(self._http)
        self.versions = VersionsService(self._http)
        self.search = SearchService(self._http)
        self.trash = TrashService(self._http)
        self.scan_reports = ScanReportsService(self._http)
        self.attestation = AttestationService(self._http)
        self.transactions = TransactionsService(self._http)
        self.templates = TemplatesService(self._http)
        self.batches = BatchesService(self._http)
        self.metadata = MetadataService(self._http)
        self.retention = RetentionService(self._http)
        self.legal_holds = LegalHoldsService(self._http)
        self.permissions = PermissionsService(self._http)
        self.comments = CommentsService(self._http)
        self.quota = QuotaService(self._http)
        self.rate_limit = RateLimitService(self._http)
        self.upload_sessions = UploadSessionsService(self._http)
        self.jobs = JobsService(self._http)
        self.activity_subscriptions = ActivitySubscriptionsService(self._http)
        self.policies = PoliciesService(self._http)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()

    def __enter__(self) -> "ConformVault":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncConformVault:
    """Asynchronous client for the ConformVault Developer API.

    Usage::

        async with AsyncConformVault("cvk_live_your_api_key") as client:
            files = await client.files.list()
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self._http = _AsyncHTTP(api_key, base_url, timeout, http_client)

        self.files = AsyncFilesService(self._http)
        self.folders = AsyncFoldersService(self._http)
        self.share_links = AsyncShareLinksService(self._http)
        self.signatures = AsyncSignaturesService(self._http)
        self.webhooks = AsyncWebhooksService(self._http)
        self.audit = AsyncAuditService(self._http)
        self.keys = AsyncKeysService(self._http)
        self.bulk = AsyncBulkService(self._http)
        self.versions = AsyncVersionsService(self._http)
        self.search = AsyncSearchService(self._http)
        self.trash = AsyncTrashService(self._http)
        self.scan_reports = AsyncScanReportsService(self._http)
        self.attestation = AsyncAttestationService(self._http)
        self.transactions = AsyncTransactionsService(self._http)
        self.templates = AsyncTemplatesService(self._http)
        self.batches = AsyncBatchesService(self._http)
        self.metadata = AsyncMetadataService(self._http)
        self.retention = AsyncRetentionService(self._http)
        self.legal_holds = AsyncLegalHoldsService(self._http)
        self.permissions = AsyncPermissionsService(self._http)
        self.comments = AsyncCommentsService(self._http)
        self.quota = AsyncQuotaService(self._http)
        self.rate_limit = AsyncRateLimitService(self._http)
        self.upload_sessions = AsyncUploadSessionsService(self._http)
        self.jobs = AsyncJobsService(self._http)
        self.activity_subscriptions = AsyncActivitySubscriptionsService(self._http)
        self.policies = AsyncPoliciesService(self._http)

    async def close(self) -> None:
        """Close the underlying async HTTP client."""
        await self._http.close()

    async def __aenter__(self) -> "AsyncConformVault":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
