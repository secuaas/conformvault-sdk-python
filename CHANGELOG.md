# Changelog

All notable changes to the ConformVault Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.1] - 2026-03-04

### Fixed
- **Policies**: paths corrected from `/policies/ip` to `/ip-policy`, `/policies/mfa` to `/mfa-policy`, `/policies/encryption-salt` to `/encryption/salt`
- **Activity Subscriptions**: path corrected from `/activity/subscriptions` to `/activity-subscriptions`
- **Comments**: rewritten from nested `/files/{id}/comments` to flat `/comments` routes; update method changed from PATCH to PUT
- **Jobs Cancel**: changed from `POST /jobs/{id}/cancel` to `DELETE /jobs/{id}`
- **Batches Cancel**: changed from `POST /batches/{id}/cancel` to `DELETE /batches/{id}`
- **Retention Update**: changed from PATCH to PUT

### Added
- `BandwidthService` / `AsyncBandwidthService` — get_summary, get_daily
- `DataExportService` / `AsyncDataExportService` — export (GDPR/Loi 25)
- `KeysService`: instant_revoke, get_revocation_status (via `/api-keys/` path)
- `BatchesService`: upload_file
- New types: `BandwidthSummary`, `DailyBandwidthStats`, `KeyRevocationStatus`, `UserDataExport`
- `file_id` field added to `CreateCommentRequest`
- Total services: 27 → 29

## [0.5.0] - 2026-03-04

### Added
- **Webhooks**: `list_deliveries`, `get_delivery`, `replay_delivery`, `re_enable`
- **Audit**: `search`, `export`, `get_stats`, `get_anomalies`
- **Files**: `get_thumbnail`, `get_scan_report`
- New service: **MetadataService** — add_tags, remove_tag, get_tags, list_by_tag, set_metadata, get_metadata, delete_metadata_key
- New service: **RetentionService** — create, list, get, update, delete
- New service: **LegalHoldsService** — create, list, get, release, add_files, remove_file
- New service: **PermissionsService** — set, get, revoke
- New service: **CommentsService** — create, list, get, update, delete, get_replies
- New service: **QuotaService** — get
- New service: **RateLimitService** — get
- New service: **UploadSessionsService** — create, upload_chunk, get_status, complete, cancel
- New service: **JobsService** — create, list, get, cancel
- New service: **ActivitySubscriptionsService** — subscribe, list, unsubscribe
- New service: **PoliciesService** — get_ip_policy, set_ip_policy, get_mfa_policy, set_mfa_policy, get_encryption_salt, set_encryption_salt
- All new services available in both sync and async variants
- 31 new type dataclasses
- Total services: 16 → 27

## [0.4.0] - 2026-03-02

### Added
- `TransactionsService` / `AsyncTransactionsService` — create, list, get, update, delete, add_item, update_item, delete_item (8 methods each)
- `TemplatesService` / `AsyncTemplatesService` — create, list, get, update, delete, generate (binary PDF), list_documents (7 methods each)
- `BatchesService` / `AsyncBatchesService` — create, list, get, commit, cancel (5 methods each)
- New types: `TransactionFolder`, `TransactionFolderItem`, `TransactionProgress`, `DocumentTemplate`, `GeneratedDocument`, `BatchOperation`, `BatchOperationItem`
- Total services: 13 → 16

## [0.3.0] - 2026-02-27

### Added
- `ScanReportsService` / `AsyncScanReportsService` — get_report, list, get_summary
- `AttestationService` / `AsyncAttestationService` — generate_loi25 (PDF stream)
- New types: `FileScanReport`, `FileScanSummary`

## [0.2.0] - 2026-02-27

### Added
- `BulkService` / `AsyncBulkService` — delete, move, download (ZIP)
- `VersionsService` / `AsyncVersionsService` — list, get, restore, delete
- `SearchService` / `AsyncSearchService` — unified search across files and folders
- `TrashService` / `AsyncTrashService` — list, restore, delete, empty
- New types: `FileVersion`, `SearchResult`, `SearchPagination`

## [0.1.0] - 2026-02-26

### Added
- Initial release with 7 services: files, folders, sharelinks, signatures, webhooks, audit, keys
- Both sync (`ConformVault`) and async (`AsyncConformVault`) clients
- Full Developer API coverage for core ConformVault operations
