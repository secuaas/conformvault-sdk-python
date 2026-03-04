"""ConformVault Python SDK — Developer API client.

Usage::

    from conformvault import ConformVault

    client = ConformVault("cvk_live_your_api_key")
    files = client.files.list()

Async usage::

    from conformvault import AsyncConformVault

    async with AsyncConformVault("cvk_live_your_api_key") as client:
        files = await client.files.list()
"""

from .client import DEFAULT_BASE_URL, VERSION, AsyncConformVault, ConformVault
from .errors import (
    APIError,
    AuthenticationError,
    ConformVaultError,
    RateLimitError,
    is_not_found,
    is_rate_limited,
)
from .types import (
    APIKey,
    ActivitySubscription,
    AddLegalHoldFilesRequest,
    AddTagsRequest,
    AuditAnomaly,
    AuditEntry,
    AuditStats,
    BandwidthSummary,
    BatchOperation,
    BatchOperationItem,
    Comment,
    CreateAPIKeyRequest,
    CreateAPIKeyResponse,
    CreateActivitySubscriptionRequest,
    CreateCommentRequest,
    CreateFolderRequest,
    CreateJobRequest,
    CreateLegalHoldRequest,
    CreateRetentionPolicyRequest,
    CreateShareLinkRequest,
    CreateSignatureRequest,
    CreateSignatureSigner,
    CreateUploadSessionRequest,
    DailyBandwidthStats,
    DataResponse,
    DocumentTemplate,
    EncryptionSalt,
    File,
    FileScanReport,
    FileScanSummary,
    FileTag,
    FileVersion,
    Folder,
    FolderPermission,
    GeneratedDocument,
    IPPolicy,
    Job,
    KeyRevocationStatus,
    LegalHold,
    LegalHoldFile,
    ListResponse,
    MFAPolicy,
    MessageResponse,
    QuotaInfo,
    RateLimitInfo,
    RegisterWebhookRequest,
    RegisterWebhookResponse,
    RetentionPolicy,
    SearchPagination,
    SearchResult,
    SetEncryptionSaltRequest,
    SetFolderPermissionRequest,
    SetIPPolicyRequest,
    SetMFAPolicyRequest,
    SetMetadataRequest,
    ShareLink,
    SignatureEnvelope,
    TransactionFolder,
    TransactionFolderItem,
    TransactionProgress,
    UpdateCommentRequest,
    UpdateRetentionPolicyRequest,
    UploadResult,
    UploadSession,
    UserDataExport,
    WebhookDelivery,
    WebhookEndpoint,
)
from .webhooks import verify_webhook_signature

__all__ = [
    # Clients
    "ConformVault",
    "AsyncConformVault",
    # Constants
    "DEFAULT_BASE_URL",
    "VERSION",
    # Errors
    "ConformVaultError",
    "APIError",
    "AuthenticationError",
    "RateLimitError",
    "is_not_found",
    "is_rate_limited",
    # Types — Files
    "File",
    "UploadResult",
    # Types — Folders
    "Folder",
    "CreateFolderRequest",
    # Types — Share Links
    "ShareLink",
    "CreateShareLinkRequest",
    # Types — Signatures
    "SignatureEnvelope",
    "CreateSignatureRequest",
    "CreateSignatureSigner",
    # Types — Webhooks
    "WebhookEndpoint",
    "WebhookDelivery",
    "RegisterWebhookRequest",
    "RegisterWebhookResponse",
    "verify_webhook_signature",
    # Types — Audit
    "AuditEntry",
    "AuditStats",
    "AuditAnomaly",
    # Types — API Keys
    "APIKey",
    "CreateAPIKeyRequest",
    "CreateAPIKeyResponse",
    # Types — File Versions
    "FileVersion",
    # Types — Search
    "SearchResult",
    "SearchPagination",
    # Types — Scan Reports
    "FileScanReport",
    "FileScanSummary",
    # Types — Transactions
    "TransactionFolder",
    "TransactionFolderItem",
    "TransactionProgress",
    # Types — Templates
    "DocumentTemplate",
    "GeneratedDocument",
    # Types — Batches
    "BatchOperation",
    "BatchOperationItem",
    # Types — Metadata & Tags
    "FileTag",
    "AddTagsRequest",
    "SetMetadataRequest",
    # Types — Retention Policies
    "RetentionPolicy",
    "CreateRetentionPolicyRequest",
    "UpdateRetentionPolicyRequest",
    # Types — Legal Holds
    "LegalHold",
    "CreateLegalHoldRequest",
    "AddLegalHoldFilesRequest",
    "LegalHoldFile",
    # Types — Folder Permissions
    "FolderPermission",
    "SetFolderPermissionRequest",
    # Types — Comments
    "Comment",
    "CreateCommentRequest",
    "UpdateCommentRequest",
    # Types — Quota
    "QuotaInfo",
    # Types — Rate Limit
    "RateLimitInfo",
    # Types — Upload Sessions
    "UploadSession",
    "CreateUploadSessionRequest",
    # Types — Jobs
    "Job",
    "CreateJobRequest",
    # Types — Activity Subscriptions
    "ActivitySubscription",
    "CreateActivitySubscriptionRequest",
    # Types — IP Policy
    "IPPolicy",
    "SetIPPolicyRequest",
    # Types — MFA Policy
    "MFAPolicy",
    "SetMFAPolicyRequest",
    # Types — Encryption Salt
    "EncryptionSalt",
    "SetEncryptionSaltRequest",
    # Types — Bandwidth
    "BandwidthSummary",
    "DailyBandwidthStats",
    # Types — Key Revocation
    "KeyRevocationStatus",
    # Types — Data Export
    "UserDataExport",
    # Types — Generic
    "ListResponse",
    "DataResponse",
    "MessageResponse",
]

__version__ = VERSION
