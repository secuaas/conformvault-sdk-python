# ConformVault Python SDK

Official Python SDK for the [ConformVault](https://conformvault.com) Developer API — secure file storage, electronic signatures, and compliance automation.

## Installation

```bash
pip install conformvault-sdk
```

**Requirements:** Python 3.9+

## Quick Start

```python
from conformvault import ConformVault

client = ConformVault("cvk_live_your_api_key")

# List files
files = client.files.list()
for f in files:
    print(f"{f.original_name} — {f.size} bytes")

# Upload a file
with open("document.pdf", "rb") as fp:
    result = client.files.upload(fp, "document.pdf", folder_id="folder-id")
    print(f"Uploaded: {result.id}")

# Download a file
content = client.files.download("file-id")
with open("downloaded.pdf", "wb") as fp:
    fp.write(content)
```

## Async Support

```python
import asyncio
from conformvault import AsyncConformVault

async def main():
    async with AsyncConformVault("cvk_live_your_api_key") as client:
        files = await client.files.list()
        print(f"Found {len(files)} files")

asyncio.run(main())
```

## Services

The SDK provides 7 service clients matching the ConformVault Developer API:

| Service | Description | Attribute |
|---------|-------------|-----------|
| **Files** | Upload, download, list, delete files | `client.files` |
| **Folders** | Create, list, get, delete folders | `client.folders` |
| **Share Links** | Create and manage share links | `client.share_links` |
| **Signatures** | Electronic signature envelopes | `client.signatures` |
| **Webhooks** | Register and manage webhook endpoints | `client.webhooks` |
| **Audit** | Query audit log entries | `client.audit` |
| **Keys** | API key self-management | `client.keys` |

## Files

```python
# List files (with optional filters)
files = client.files.list(folder_id="folder-id", page=1, limit=20)

# Get file metadata
file = client.files.get("file-id")

# Upload
result = client.files.upload(open("doc.pdf", "rb"), "doc.pdf")

# Download
content = client.files.download("file-id")

# Delete
client.files.delete("file-id")
```

## Folders

```python
from conformvault import CreateFolderRequest

folders = client.folders.list(parent_id="parent-id")
folder = client.folders.get("folder-id")
new_folder = client.folders.create(CreateFolderRequest(name="Reports"))
client.folders.delete("folder-id")
```

## Share Links

```python
from conformvault import CreateShareLinkRequest

links = client.share_links.list()
link = client.share_links.create(CreateShareLinkRequest(
    file_id="file-id",
    type="download",
    expires_in=86400,  # 24 hours
))
client.share_links.delete("link-id")
```

## Electronic Signatures

```python
from conformvault import CreateSignatureRequest, CreateSignatureSigner

envelope = client.signatures.create(CreateSignatureRequest(
    file_id="file-id",
    subject="Please sign this NDA",
    signers=[
        CreateSignatureSigner(email="signer@example.com", name="Jane Doe", role="signer"),
    ],
    expiry_days=30,
))

status = client.signatures.get_status(envelope.id)
signed_pdf = client.signatures.download_signed(envelope.id)
client.signatures.revoke(envelope.id)
```

## Webhooks

```python
from conformvault import RegisterWebhookRequest, verify_webhook_signature

# Register
resp = client.webhooks.register(RegisterWebhookRequest(
    url="https://your-app.com/webhooks/conformvault",
    events=["file.uploaded", "signature.completed"],
))
print(f"Secret (save this!): {resp.secret}")

# List / delete / test
hooks = client.webhooks.list()
client.webhooks.test("webhook-id")
client.webhooks.delete("webhook-id")

# Verify incoming webhook signature
is_valid = verify_webhook_signature(
    payload=request_body,
    signature_header=request.headers["X-Webhook-Signature"],
    secret="whsec_your_secret",
)
```

## Audit Logs

```python
entries = client.audit.list(
    event_type="file.uploaded",
    from_date="2025-01-01",
    to_date="2025-12-31",
    page=1,
    limit=50,
)
```

## API Keys

```python
from conformvault import CreateAPIKeyRequest

keys = client.keys.list()
new_key = client.keys.create(CreateAPIKeyRequest(
    name="CI/CD Key",
    environment="test",
    scopes=["files:read", "files:write"],
))
print(f"Key (save this!): {new_key.key}")

key = client.keys.get("key-id")
rotated = client.keys.rotate("key-id")
client.keys.revoke("key-id")
```

## Error Handling

```python
from conformvault import APIError, AuthenticationError, RateLimitError, is_not_found

try:
    file = client.files.get("nonexistent")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited — retry after {e.retry_after}s")
except APIError as e:
    if is_not_found(e):
        print("File not found")
    else:
        print(f"API error {e.status_code}: {e.message}")
```

## Configuration

```python
import httpx
from conformvault import ConformVault

client = ConformVault(
    "cvk_live_your_api_key",
    base_url="https://custom-api.example.com/dev/v1",  # custom base URL
    timeout=60.0,                                       # request timeout in seconds
    http_client=httpx.Client(proxies="http://proxy:8080"),  # custom httpx client
)
```

## API Base URL

| Environment | URL |
|-------------|-----|
| Production | `https://api.conformvault.com/dev/v1` (default) |

## Authentication

All requests use Bearer token authentication:

```
Authorization: Bearer cvk_live_xxx
```

API keys prefixed with `cvk_live_` are for production; `cvk_test_` for sandbox.

## License

MIT — see [LICENSE](LICENSE).
