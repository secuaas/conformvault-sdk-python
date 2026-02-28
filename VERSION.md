# Historique des Versions - ConformVault Python SDK

## Version Actuelle
**0.2.0** - 2026-02-27

---

## Versions

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
