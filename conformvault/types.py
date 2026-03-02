"""Data models for the ConformVault Python SDK.

All models use dataclasses with type hints.  Optional fields default to
``None``.  Datetime strings from the API are kept as ``str`` so callers
can parse them with ``datetime.fromisoformat()`` when needed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, List, Optional, TypeVar

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Generic response wrappers
# ---------------------------------------------------------------------------

@dataclass
class ListResponse(Generic[T]):
    """Wraps a paginated list response from the API."""

    data: List[T] = field(default_factory=list)


@dataclass
class DataResponse(Generic[T]):
    """Wraps a single-item response from the API."""

    data: Optional[T] = None


@dataclass
class MessageResponse:
    """Wraps a simple message response from the API."""

    message: str = ""


# ---------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------

@dataclass
class File:
    """A stored file."""

    id: str = ""
    name: str = ""
    original_name: str = ""
    size: int = 0
    content_type: str = ""
    folder_id: Optional[str] = None
    created_at: str = ""


@dataclass
class UploadResult:
    """Response from uploading a file."""

    id: str = ""
    name: str = ""
    original_name: str = ""
    size: int = 0
    created_at: str = ""


# ---------------------------------------------------------------------------
# Folders
# ---------------------------------------------------------------------------

@dataclass
class Folder:
    """A folder in the file tree."""

    id: str = ""
    name: str = ""
    path: str = ""
    parent_id: Optional[str] = None
    created_at: str = ""


@dataclass
class CreateFolderRequest:
    """Input for creating a folder."""

    name: str = ""
    parent_id: Optional[str] = None


# ---------------------------------------------------------------------------
# Share Links
# ---------------------------------------------------------------------------

@dataclass
class ShareLink:
    """A share link."""

    id: str = ""
    token: str = ""
    url: str = ""
    type: str = ""  # "download" or "upload"
    expires_at: str = ""
    is_active: bool = False
    created_at: str = ""


@dataclass
class CreateShareLinkRequest:
    """Input for creating a share link."""

    file_id: Optional[str] = None
    folder_id: Optional[str] = None
    type: str = ""
    expires_in: Optional[int] = None  # seconds
    password: Optional[str] = None


# ---------------------------------------------------------------------------
# Signatures
# ---------------------------------------------------------------------------

@dataclass
class SignatureEnvelope:
    """A signature envelope."""

    id: str = ""
    provider: str = ""
    status: str = ""
    subject: str = ""
    message: Optional[str] = None
    source_file_id: Optional[str] = None
    signed_file_id: Optional[str] = None
    expiry_days: int = 0
    created_at: str = ""


@dataclass
class CreateSignatureSigner:
    """A signer in a create-signature request."""

    email: str = ""
    name: str = ""
    role: str = ""
    sign_order: int = 0


@dataclass
class CreateSignatureRequest:
    """Input for creating a signature envelope."""

    file_id: str = ""
    subject: str = ""
    message: Optional[str] = None
    signers: List[CreateSignatureSigner] = field(default_factory=list)
    expiry_days: int = 0


# ---------------------------------------------------------------------------
# Webhooks
# ---------------------------------------------------------------------------

@dataclass
class WebhookEndpoint:
    """A registered webhook endpoint."""

    id: str = ""
    url: str = ""
    events: List[str] = field(default_factory=list)
    environment: str = ""
    is_active: bool = False
    created_at: str = ""


@dataclass
class RegisterWebhookRequest:
    """Input for registering a webhook endpoint."""

    url: str = ""
    events: Optional[List[str]] = None
    environment: str = ""


@dataclass
class RegisterWebhookResponse:
    """Response from registering a webhook; includes the signing secret."""

    id: str = ""
    url: str = ""
    events: List[str] = field(default_factory=list)
    environment: str = ""
    is_active: bool = False
    created_at: str = ""
    secret: str = ""


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------

@dataclass
class AuditEntry:
    """An audit log entry."""

    id: str = ""
    action: str = ""
    resource_type: str = ""
    resource_id: str = ""
    details: Optional[Any] = None
    created_at: str = ""


# ---------------------------------------------------------------------------
# API Keys
# ---------------------------------------------------------------------------

@dataclass
class APIKey:
    """A developer API key."""

    id: str = ""
    name: str = ""
    prefix: str = ""
    environment: str = ""
    scopes: List[str] = field(default_factory=list)
    expires_at: Optional[str] = None
    created_at: str = ""


@dataclass
class CreateAPIKeyRequest:
    """Input for creating an API key."""

    name: str = ""
    environment: str = ""
    scopes: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# File Versions
# ---------------------------------------------------------------------------

@dataclass
class FileVersion:
    """A version of a file."""

    id: str = ""
    file_id: str = ""
    version: int = 0
    size: int = 0
    created_at: str = ""


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

@dataclass
class SearchResult:
    """A single search result."""

    id: str = ""
    type: str = ""  # "file" or "folder"
    name: str = ""
    path: str = ""
    size: int = 0
    content_type: str = ""
    created_at: str = ""


@dataclass
class SearchPagination:
    """Pagination metadata for search results."""

    page: int = 0
    page_size: int = 0
    total: int = 0


@dataclass
class CreateAPIKeyResponse:
    """Response from creating an API key; includes the full key (shown once)."""

    id: str = ""
    name: str = ""
    prefix: str = ""
    environment: str = ""
    scopes: List[str] = field(default_factory=list)
    expires_at: Optional[str] = None
    created_at: str = ""
    key: str = ""


# ---------------------------------------------------------------------------
# Scan Reports
# ---------------------------------------------------------------------------

@dataclass
class FileScanReport:
    """A ClamAV scan report for a file."""

    id: str = ""
    file_id: str = ""
    organization_id: str = ""
    scan_engine: str = ""
    engine_version: Optional[str] = None
    scan_status: str = ""
    threat_name: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    scan_duration_ms: Optional[int] = None
    scanned_at: str = ""


@dataclass
class FileScanSummary:
    """Summary of scan statistics for an organization."""

    total_scans: int = 0
    clean_count: int = 0
    infected_count: int = 0
    error_count: int = 0
    skipped_count: int = 0
    scan_engine: str = ""
    engine_version: str = ""


# ---------------------------------------------------------------------------
# Transaction Folders
# ---------------------------------------------------------------------------

@dataclass
class TransactionProgress:
    """Completion statistics for a transaction folder."""

    total: int = 0
    completed: int = 0
    pending: int = 0


@dataclass
class TransactionFolderItem:
    """A single item in a transaction folder."""

    id: str = ""
    transaction_id: str = ""
    label: str = ""
    description: Optional[str] = None
    required: bool = False
    status: str = ""
    file_id: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class TransactionFolder:
    """A transaction folder."""

    id: str = ""
    name: str = ""
    description: Optional[str] = None
    status: str = ""
    due_date: Optional[str] = None
    progress: Optional[Any] = None
    items: List[Any] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""


# ---------------------------------------------------------------------------
# Document Templates
# ---------------------------------------------------------------------------

@dataclass
class DocumentTemplate:
    """A document template."""

    id: str = ""
    name: str = ""
    description: Optional[str] = None
    content_type: str = ""
    fields: List[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""


@dataclass
class GeneratedDocument:
    """A document generated from a template."""

    id: str = ""
    template_id: str = ""
    name: str = ""
    size: int = 0
    status: str = ""
    file_id: str = ""
    created_at: str = ""


# ---------------------------------------------------------------------------
# Batch Operations
# ---------------------------------------------------------------------------

@dataclass
class BatchOperationItem:
    """A single item within a batch operation."""

    id: str = ""
    index: int = 0
    filename: str = ""
    size: int = 0
    mime_type: str = ""
    status: str = ""
    file_id: Optional[str] = None
    error: Optional[str] = None


@dataclass
class BatchOperation:
    """A batch operation."""

    id: str = ""
    status: str = ""
    type: str = ""
    total: int = 0
    completed: int = 0
    failed: int = 0
    items: List[Any] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
