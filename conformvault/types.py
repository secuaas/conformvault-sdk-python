"""Data models for the ConformVault Python SDK.

All models use dataclasses with type hints.  Optional fields default to
``None``.  Datetime strings from the API are kept as ``str`` so callers
can parse them with ``datetime.fromisoformat()`` when needed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Generic, List, Optional, TypeVar

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


# ---------------------------------------------------------------------------
# Webhook Deliveries
# ---------------------------------------------------------------------------

@dataclass
class WebhookDelivery:
    """A webhook delivery attempt."""

    id: str = ""
    webhook_id: str = ""
    event_type: str = ""
    status: str = ""
    http_status: int = 0
    request_body: str = ""
    response_body: str = ""
    created_at: str = ""
    delivered_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Audit extended types
# ---------------------------------------------------------------------------

@dataclass
class AuditStats:
    """Audit log statistics."""

    total_events: int = 0
    events_by_type: Optional[Dict[str, int]] = None
    events_by_day: Optional[Dict[str, int]] = None


@dataclass
class AuditAnomaly:
    """An audit anomaly detection."""

    id: str = ""
    type: str = ""
    description: str = ""
    severity: str = ""
    detected_at: str = ""


# ---------------------------------------------------------------------------
# File Metadata & Tags
# ---------------------------------------------------------------------------

@dataclass
class FileTag:
    """A tag on a file."""

    tag: str = ""
    created_at: str = ""


@dataclass
class AddTagsRequest:
    """Input for adding tags to a file."""

    tags: List[str] = field(default_factory=list)


@dataclass
class SetMetadataRequest:
    """Input for setting custom metadata on a file."""

    metadata: Optional[Dict[str, str]] = None


# ---------------------------------------------------------------------------
# Retention Policies
# ---------------------------------------------------------------------------

@dataclass
class RetentionPolicy:
    """A retention policy."""

    id: str = ""
    name: str = ""
    retention_days: int = 0
    auto_delete: bool = False
    created_at: str = ""
    updated_at: str = ""


@dataclass
class CreateRetentionPolicyRequest:
    """Input for creating a retention policy."""

    name: str = ""
    retention_days: int = 0
    auto_delete: bool = False


@dataclass
class UpdateRetentionPolicyRequest:
    """Input for updating a retention policy."""

    name: Optional[str] = None
    retention_days: Optional[int] = None
    auto_delete: Optional[bool] = None


# ---------------------------------------------------------------------------
# Legal Holds
# ---------------------------------------------------------------------------

@dataclass
class LegalHold:
    """A legal hold."""

    id: str = ""
    name: str = ""
    description: str = ""
    status: str = ""
    file_count: int = 0
    created_at: str = ""
    released_at: Optional[str] = None


@dataclass
class CreateLegalHoldRequest:
    """Input for creating a legal hold."""

    name: str = ""
    description: Optional[str] = None


@dataclass
class AddLegalHoldFilesRequest:
    """Input for adding files to a legal hold."""

    file_ids: List[str] = field(default_factory=list)


@dataclass
class LegalHoldFile:
    """A file within a legal hold."""

    file_id: str = ""
    added_at: str = ""


# ---------------------------------------------------------------------------
# Folder Permissions
# ---------------------------------------------------------------------------

@dataclass
class FolderPermission:
    """A folder permission entry."""

    folder_id: str = ""
    user_id: str = ""
    permission: str = ""
    granted_at: str = ""


@dataclass
class SetFolderPermissionRequest:
    """Input for setting a folder permission."""

    user_id: str = ""
    permission: str = ""


# ---------------------------------------------------------------------------
# Comments
# ---------------------------------------------------------------------------

@dataclass
class Comment:
    """A comment on a file."""

    id: str = ""
    file_id: str = ""
    content: str = ""
    author_id: str = ""
    parent_id: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""


@dataclass
class CreateCommentRequest:
    """Input for creating a comment."""

    file_id: str = ""
    content: str = ""
    parent_id: Optional[str] = None


@dataclass
class UpdateCommentRequest:
    """Input for updating a comment."""

    content: str = ""


# ---------------------------------------------------------------------------
# Quota
# ---------------------------------------------------------------------------

@dataclass
class QuotaInfo:
    """Quota usage information."""

    used_bytes: int = 0
    total_bytes: int = 0
    file_count: int = 0
    max_file_count: int = 0


# ---------------------------------------------------------------------------
# Rate Limit
# ---------------------------------------------------------------------------

@dataclass
class RateLimitInfo:
    """Rate limit status information."""

    requests_per_minute: int = 0
    requests_remaining: int = 0
    reset_at: str = ""


# ---------------------------------------------------------------------------
# Upload Sessions
# ---------------------------------------------------------------------------

@dataclass
class UploadSession:
    """A chunked upload session."""

    id: str = ""
    filename: str = ""
    total_size: int = 0
    chunk_size: int = 0
    chunks_uploaded: int = 0
    total_chunks: int = 0
    status: str = ""
    created_at: str = ""
    expires_at: str = ""


@dataclass
class CreateUploadSessionRequest:
    """Input for creating a chunked upload session."""

    filename: str = ""
    total_size: int = 0
    content_type: Optional[str] = None
    folder_id: Optional[str] = None


# ---------------------------------------------------------------------------
# Jobs
# ---------------------------------------------------------------------------

@dataclass
class Job:
    """A background job."""

    id: str = ""
    type: str = ""
    status: str = ""
    progress: int = 0
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: str = ""
    completed_at: Optional[str] = None


@dataclass
class CreateJobRequest:
    """Input for creating a background job."""

    type: str = ""
    params: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# Activity Subscriptions
# ---------------------------------------------------------------------------

@dataclass
class ActivitySubscription:
    """An activity event subscription."""

    id: str = ""
    event_types: List[str] = field(default_factory=list)
    callback_url: str = ""
    created_at: str = ""


@dataclass
class CreateActivitySubscriptionRequest:
    """Input for creating an activity subscription."""

    event_types: List[str] = field(default_factory=list)
    callback_url: str = ""


# ---------------------------------------------------------------------------
# IP Policy
# ---------------------------------------------------------------------------

@dataclass
class IPPolicy:
    """IP access policy."""

    enabled: bool = False
    allowed_ips: List[str] = field(default_factory=list)
    denied_ips: List[str] = field(default_factory=list)


@dataclass
class SetIPPolicyRequest:
    """Input for setting IP access policy."""

    enabled: bool = False
    allowed_ips: Optional[List[str]] = None
    denied_ips: Optional[List[str]] = None


# ---------------------------------------------------------------------------
# MFA Policy
# ---------------------------------------------------------------------------

@dataclass
class MFAPolicy:
    """MFA policy configuration."""

    enabled: bool = False
    required_for: List[str] = field(default_factory=list)


@dataclass
class SetMFAPolicyRequest:
    """Input for setting MFA policy."""

    enabled: bool = False
    required_for: Optional[List[str]] = None


# ---------------------------------------------------------------------------
# Encryption Salt
# ---------------------------------------------------------------------------

@dataclass
class EncryptionSalt:
    """Encryption salt value."""

    salt: str = ""


@dataclass
class SetEncryptionSaltRequest:
    """Input for setting encryption salt."""

    salt: str = ""


# ---------------------------------------------------------------------------
# Bandwidth Analytics
# ---------------------------------------------------------------------------

@dataclass
class BandwidthSummary:
    """Bandwidth usage summary."""
    total_upload_bytes: int = 0
    total_download_bytes: int = 0
    period: str = ""

@dataclass
class DailyBandwidthStats:
    """Daily bandwidth statistics."""
    date: str = ""
    upload_bytes: int = 0
    download_bytes: int = 0

# ---------------------------------------------------------------------------
# Key Revocation
# ---------------------------------------------------------------------------

@dataclass
class KeyRevocationStatus:
    """API key revocation status."""
    key_id: str = ""
    revoked: bool = False
    revoked_at: Optional[str] = None

# ---------------------------------------------------------------------------
# Data Export
# ---------------------------------------------------------------------------

@dataclass
class UserDataExport:
    """User data export package (GDPR/Loi 25)."""
    user_id: str = ""
    status: str = ""
    url: Optional[str] = None
    expires_at: Optional[str] = None
    created_at: str = ""
