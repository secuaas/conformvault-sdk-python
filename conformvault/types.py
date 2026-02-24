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
