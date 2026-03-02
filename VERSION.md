# Historique des Versions - ConformVault Python SDK

## Version Actuelle
**0.4.0** - 2026-03-02

---

## Versions

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
