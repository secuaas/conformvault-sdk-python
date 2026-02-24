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
    AuditEntry,
    CreateAPIKeyRequest,
    CreateAPIKeyResponse,
    CreateFolderRequest,
    CreateShareLinkRequest,
    CreateSignatureRequest,
    CreateSignatureSigner,
    DataResponse,
    File,
    Folder,
    ListResponse,
    MessageResponse,
    RegisterWebhookRequest,
    RegisterWebhookResponse,
    ShareLink,
    SignatureEnvelope,
    UploadResult,
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
    "RegisterWebhookRequest",
    "RegisterWebhookResponse",
    "verify_webhook_signature",
    # Types — Audit
    "AuditEntry",
    # Types — API Keys
    "APIKey",
    "CreateAPIKeyRequest",
    "CreateAPIKeyResponse",
    # Types — Generic
    "ListResponse",
    "DataResponse",
    "MessageResponse",
]

__version__ = VERSION
