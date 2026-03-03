# Changelog

All notable changes to the ConformVault Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
