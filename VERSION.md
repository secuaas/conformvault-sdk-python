# Historique des Versions - ConformVault Python SDK

## Version Actuelle
**0.5.1** - 2026-03-04

---

## Versions

### 0.5.1 - 2026-03-04
**Commit:** `pending`
**Type:** Patch - Fix 9 route mismatches + add 6 missing routes (backend alignment)

### Corrigé
- **Policies**: `/policies/ip` → `/ip-policy`, `/policies/mfa` → `/mfa-policy`, `/policies/encryption-salt` → `/encryption/salt`
- **Activity Subscriptions**: `/activity/subscriptions` → `/activity-subscriptions`
- **Comments**: Rewritten from nested `/files/{id}/comments` to flat `/comments` routes; `file_id` moved to request body/query param; update changed from PATCH to PUT
- **Jobs Cancel**: `POST /jobs/{id}/cancel` → `DELETE /jobs/{id}`
- **Batches Cancel**: `POST /batches/{id}/cancel` → `DELETE /batches/{id}`
- **Retention Update**: PATCH → PUT

### Ajouté
- **`bandwidth.py`**: `BandwidthService` / `AsyncBandwidthService` — get_summary, get_daily (2 methods each)
- **`data_export.py`**: `DataExportService` / `AsyncDataExportService` — export (1 method each) for GDPR/Loi 25
- **`keys.py`**: instant_revoke, get_revocation_status (2 new methods via `/api-keys/` path, sync+async)
- **`batches.py`**: upload_file (1 new method, sync+async)
- New types: `BandwidthSummary`, `DailyBandwidthStats`, `KeyRevocationStatus`, `UserDataExport`
- `file_id` field added to `CreateCommentRequest`
- Total services: 27 → 29

### Tests effectués
- ✅ `python3 -c "import conformvault"` — success

---

### 0.5.0 - 2026-03-04
**Commit:** `pending`
**Type:** Minor - SDK v0.5.0: 57 new methods (sync+async) across 11 new services (~85% API coverage)

### Ajouté
- **Webhooks**: `list_deliveries`, `get_delivery`, `replay_delivery`, `re_enable` (4 methods × sync+async)
- **Audit**: `search`, `export` (stream), `get_stats`, `get_anomalies` (4 methods × sync+async)
- **Files**: `get_thumbnail` (stream), `get_scan_report` (2 methods × sync+async)
- **`metadata.py`**: `MetadataService` / `AsyncMetadataService` — add_tags, remove_tag, get_tags, list_by_tag, set_metadata, get_metadata, delete_metadata_key (7 methods each)
- **`retention.py`**: `RetentionService` / `AsyncRetentionService` — create, list, get, update, delete (5 methods each)
- **`legal_holds.py`**: `LegalHoldsService` / `AsyncLegalHoldsService` — create, list, get, release, add_files, remove_file (6 methods each)
- **`permissions.py`**: `PermissionsService` / `AsyncPermissionsService` — set, get, revoke (3 methods each)
- **`comments.py`**: `CommentsService` / `AsyncCommentsService` — create, list, get, update, delete, get_replies (6 methods each)
- **`quota.py`**: `QuotaService` + `RateLimitService` (sync+async) — get (1 method each)
- **`upload_sessions.py`**: `UploadSessionsService` / `AsyncUploadSessionsService` — create, upload_chunk, get_status, complete, cancel (5 methods each)
- **`jobs.py`**: `JobsService` / `AsyncJobsService` — create, list, get, cancel (4 methods each)
- **`activity_subscriptions.py`**: `ActivitySubscriptionsService` / `AsyncActivitySubscriptionsService` — subscribe, list, unsubscribe (3 methods each)
- **`policies.py`**: `PoliciesService` / `AsyncPoliciesService` — get_ip_policy, set_ip_policy, get_mfa_policy, set_mfa_policy, get_encryption_salt, set_encryption_salt (6 methods each)
- 31 new dataclass types in `types.py`
- All types exported from `__init__.py`
- Version bumped to 0.5.0
- Total services: 16 → 27

### Tests effectués
- ✅ `python3 -c "import conformvault"` — success
- ✅ All 27 services verified on sync client

---

### 0.4.1 - 2026-03-03
**Commit:** `5494f69`
**Type:** Patch - Add CHANGELOG.md

### Ajouté
- `CHANGELOG.md` — Keep a Changelog format, extracted from VERSION.md history

### Tests effectués
- ✅ `python3 -c "import conformvault"` — success

---

### 0.4.0 - 2026-03-02
**Commit:** `da2d78f`
**Type:** Minor - Transactions, Templates, Batches services

### Ajouté
- **`transactions.py`**: `TransactionsService` / `AsyncTransactionsService` — create, list, get, update, delete, add_item, update_item, delete_item (8 methods each)
- **`templates.py`**: `TemplatesService` / `AsyncTemplatesService` — create, list, get, update, delete, generate (binary PDF), list_documents (7 methods each)
- **`batches.py`**: `BatchesService` / `AsyncBatchesService` — create, list, get, commit, cancel (5 methods each)
- New types in `types.py`: `TransactionFolder`, `TransactionFolderItem`, `TransactionProgress`, `DocumentTemplate`, `GeneratedDocument`, `BatchOperation`, `BatchOperationItem`
- Services registered as `client.transactions`, `client.templates`, `client.batches` in both `ConformVault` and `AsyncConformVault`
- Types exported from `__init__.py`
- Total services: 13 → 16

### Tests effectués
- ✅ `python3 -c "import conformvault"` — success
- ✅ 16 services verified on sync client

---

### 0.3.0 - 2026-02-27
**Type:** Minor - ScanReports and Attestation services

### Ajouté
- **`scan_reports.py`**: `ScanReportsService` / `AsyncScanReportsService` — `get_report(file_id)`, `list(limit, offset)`, `get_summary()`
- **`attestation.py`**: `AttestationService` / `AsyncAttestationService` — `generate_loi25()` → bytes (PDF)
- New types: `FileScanReport`, `FileScanSummary` in `types.py`
- Services registered as `client.scan_reports` and `client.attestation` in both `ConformVault` and `AsyncConformVault`
- Types exported from `__init__.py`
- VERSION bumped to `0.3.0`

### Tests effectués
- ✅ `python3 -c "from conformvault import ConformVault; print('OK')"` — success
- ✅ Full smoke test: all service attributes, type fields, async client verified

---

### 0.2.0 - 2026-02-27
**Type:** Minor - V2-4 SDK expansion: bulk, versions, search, trash services

### Ajouté
- **`bulk.py`**: `BulkService` / `AsyncBulkService` — delete, move, download (ZIP)
- **`versions.py`**: `VersionsService` / `AsyncVersionsService` — list, get, restore, delete
- **`search.py`**: `SearchService` / `AsyncSearchService` — unified search across files and folders
- **`trash.py`**: `TrashService` / `AsyncTrashService` — list, restore, delete, empty
- New types: `FileVersion`, `SearchResult`, `SearchPagination`
- Services registered in `ConformVault` and `AsyncConformVault` clients
- Types exported from `__init__.py`

### Tests effectués
- ✅ `python3 -c "from conformvault import ConformVault"` — success

### 0.1.0 - 2026-02-26
**Type:** Initial release — 7 services (files, folders, sharelinks, signatures, webhooks, audit, keys)
