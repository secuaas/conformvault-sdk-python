# Historique des Versions - ConformVault Python SDK

## Version Actuelle
**0.3.0** - 2026-02-27

---

## Versions

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
