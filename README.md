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

The SDK provides 27 service clients matching the ConformVault Developer API:

| Service | Methods | Attribute |
|---------|---------|-----------|
| **Files** | `list`, `get`, `upload`, `download`, `delete`, `get_thumbnail`, `get_scan_report` | `client.files` |
| **Folders** | `list`, `get`, `create`, `delete` | `client.folders` |
| **Share Links** | `list`, `create`, `delete` | `client.share_links` |
| **Signatures** | `create`, `get_status`, `download_signed`, `revoke` | `client.signatures` |
| **Webhooks** | `list`, `register`, `test`, `delete` | `client.webhooks` |
| **Audit** | `list`, `search`, `export` | `client.audit` |
| **Keys** | `list`, `get`, `create`, `rotate`, `revoke` | `client.keys` |
| **Bulk** | `delete`, `move`, `download` | `client.bulk` |
| **Versions** | `list`, `get`, `restore`, `delete` | `client.versions` |
| **Search** | `search` | `client.search` |
| **Trash** | `list`, `restore`, `delete`, `empty` | `client.trash` |
| **Scan Reports** | `get_report`, `list`, `get_summary` | `client.scan_reports` |
| **Attestation** | `generate_loi25` | `client.attestation` |
| **Transactions** | `create`, `get`, `add_item`, `delete` | `client.transactions` |
| **Templates** | `create`, `generate` | `client.templates` |
| **Batches** | `create`, `get`, `commit`, `cancel` | `client.batches` |
| **Metadata** | `add_tags`, `get_tags`, `list_by_tag`, `remove_tag`, `set_metadata`, `get_metadata`, `delete_metadata_key` | `client.metadata` |
| **Retention** | `list`, `create`, `delete` | `client.retention` |
| **Legal Holds** | `create`, `add_files`, `release` | `client.legal_holds` |
| **Permissions** | `get`, `set`, `revoke` | `client.permissions` |
| **Comments** | `list`, `create`, `get_replies`, `delete` | `client.comments` |
| **Quota** | `get` | `client.quota` |
| **Rate Limit** | `get` | `client.rate_limit` |
| **Upload Sessions** | `create`, `upload_chunk`, `complete` | `client.upload_sessions` |
| **Jobs** | `create`, `get`, `cancel` | `client.jobs` |
| **Activity Subscriptions** | `list`, `subscribe`, `unsubscribe` | `client.activity_subscriptions` |
| **Policies** | `get_ip_policy`, `set_ip_policy`, `set_mfa_policy`, `get_encryption_salt`, `set_encryption_salt` | `client.policies` |

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

## Bulk Operations

```python
result = client.bulk.delete(["file-1", "file-2", "file-3"])
print(f"Deleted {result.succeeded}/{result.processed}")

result = client.bulk.move(["file-1", "file-2"], "target-folder-id")

# Download as ZIP
zip_data = client.bulk.download(["file-1", "file-2"])
```

## File Versions

```python
versions = client.versions.list("file-id")
version = client.versions.get("file-id", "version-id")
client.versions.restore("file-id", "version-id")
client.versions.delete("file-id", "version-id")
```

## Search

```python
results = client.search.search(query="quarterly report", types="files,folders", page=1)
```

## Trash

```python
trashed = client.trash.list(page=1, limit=50)
client.trash.restore("file-id")
client.trash.delete("file-id")
result = client.trash.empty()
```

## Scan Reports

```python
report = client.scan_reports.get_report("file-id")
reports = client.scan_reports.list(limit=50)
summary = client.scan_reports.get_summary()
```

## Compliance Attestation

```python
pdf_bytes = client.attestation.generate_loi25()
with open("attestation.pdf", "wb") as f:
    f.write(pdf_bytes)
```

## Transaction Folders

```python
from conformvault import CreateTransactionRequest, CreateTransactionItemRequest

tx = client.transactions.create(name="Real Estate Closing Q1", due_date="2025-06-30")
item = client.transactions.add_item(tx.id, CreateTransactionItemRequest(
    label="Signed purchase agreement", required=True,
))
tx = client.transactions.get(tx.id)
print(f"Progress: {tx.progress.completed}/{tx.progress.total}")
client.transactions.delete(tx.id)
```

## Document Templates

```python
from conformvault import CreateTemplateRequest, GenerateDocumentRequest

tmpl = client.templates.create(CreateTemplateRequest(
    name="Invoice", content_type="application/pdf", fields=["client", "amount"],
))
pdf = client.templates.generate(tmpl.id, GenerateDocumentRequest(
    data={"client": "Acme Corp", "amount": "$5,000"},
))
```

## Batch Operations

```python
from conformvault import CreateBatchRequest

batch = client.batches.create(CreateBatchRequest(type="upload", folder_id="folder-id"))
batch = client.batches.commit(batch.id)
batch = client.batches.get(batch.id)
client.batches.cancel(batch.id)
```

## File Metadata & Tags

```python
from conformvault import AddTagsRequest, SetMetadataRequest

# Tags
client.metadata.add_tags("file-id", AddTagsRequest(tags=["confidential", "legal"]))
tags = client.metadata.get_tags("file-id")
files = client.metadata.list_by_tag("confidential")
client.metadata.remove_tag("file-id", "legal")

# Metadata
client.metadata.set_metadata("file-id", SetMetadataRequest(
    metadata={"department": "legal", "case": "2025-001"},
))
meta = client.metadata.get_metadata("file-id")
client.metadata.delete_metadata_key("file-id", "case")
```

## Retention Policies

```python
from conformvault import CreateRetentionPolicyRequest

policy = client.retention.create(CreateRetentionPolicyRequest(
    name="7-Year Hold", retention_days=2555, auto_delete=False,
))
policies = client.retention.list()
client.retention.delete(policy.id)
```

## Legal Holds

```python
from conformvault import CreateLegalHoldRequest, AddLegalHoldFilesRequest

hold = client.legal_holds.create(CreateLegalHoldRequest(
    name="Case 2025-001", description="Litigation hold",
))
client.legal_holds.add_files(hold.id, AddLegalHoldFilesRequest(
    file_ids=["file-1", "file-2"],
))
client.legal_holds.release(hold.id)
```

## Folder Permissions

```python
from conformvault import SetFolderPermissionRequest

client.permissions.set("folder-id", SetFolderPermissionRequest(
    user_id="user-id", permission="write",
))
perms = client.permissions.get("folder-id")
client.permissions.revoke("folder-id", "user-id")
```

## Comments

```python
from conformvault import CreateCommentRequest

comment = client.comments.create("file-id", CreateCommentRequest(
    content="Please review before signing.",
))
comments = client.comments.list("file-id")
replies = client.comments.get_replies("file-id", comment.id)
client.comments.delete("file-id", comment.id)
```

## Quota & Rate Limits

```python
quota = client.quota.get()
print(f"Used: {quota.used_bytes}/{quota.total_bytes} bytes")

rl = client.rate_limit.get()
print(f"Remaining: {rl.requests_remaining}/{rl.requests_per_minute}")
```

## Upload Sessions

```python
from conformvault import CreateUploadSessionRequest

session = client.upload_sessions.create(CreateUploadSessionRequest(
    filename="large-file.zip", total_size=5_000_000_000,
))
for i, chunk in enumerate(chunks):
    client.upload_sessions.upload_chunk(session.id, i, chunk)
file = client.upload_sessions.complete(session.id)
```

## Background Jobs

```python
from conformvault import CreateJobRequest

job = client.jobs.create(CreateJobRequest(type="export", params={"format": "zip"}))
job = client.jobs.get(job.id)
print(f"Status: {job.status} ({job.progress}%)")
client.jobs.cancel(job.id)
```

## Activity Subscriptions

```python
from conformvault import CreateActivitySubscriptionRequest

sub = client.activity_subscriptions.subscribe(CreateActivitySubscriptionRequest(
    event_types=["file.uploaded", "file.deleted"],
    callback_url="https://your-app.com/activity",
))
subs = client.activity_subscriptions.list()
client.activity_subscriptions.unsubscribe(sub.id)
```

## Security Policies

```python
from conformvault import SetIPPolicyRequest, SetMFAPolicyRequest, SetEncryptionSaltRequest

# IP Policy
ip_policy = client.policies.get_ip_policy()
client.policies.set_ip_policy(SetIPPolicyRequest(
    enabled=True, allowed_ips=["203.0.113.0/24"],
))

# MFA Policy
client.policies.set_mfa_policy(SetMFAPolicyRequest(
    enabled=True, required_for=["file.delete", "settings.update"],
))

# Encryption Salt
salt = client.policies.get_encryption_salt()
client.policies.set_encryption_salt(SetEncryptionSaltRequest(salt="base64-salt"))
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
