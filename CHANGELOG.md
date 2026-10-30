# Changelog

## 2.0.0 — 2026-10-30

### Přidáno
- **Sdílení mezi uživateli Home Assistantu:** add-on má Flask API + SQLite v `/data`, seznamy jsou společné pro všechny uživatele a zařízení.
- Synchronizace každých 5 s, okamžitě po návratu do aplikace; konflikty se řeší podle `updatedAt` seznamu.
- Tombstones pro smazané seznamy, stav uložený i v `localStorage` jako offline záloha.
- Patička ukazuje, zda je seznam společný, a kdo naposledy upravoval.
- `backend/app.py` (GET/PUT `/api/state`, `/healthz`), `backend/requirements.txt`.
- Add-on přesunut z nginx na `python:3.12-alpine` (`run.sh`, data v `/data`).

## 1.1.0 — 2026-10-30

### Přidáno
- Rychlé přidání položky: pole + tlačítko **+** (a Enter) přímo na seznamu, s volbou obchodu.
- Tlačítko **−** u každé položky pro okamžité odebrání.
- Home Assistant add-on (`addon/`, `repository.yaml`), ingress, port 8091, ikony.

## 1.0.0 — 2026-06-04

- První verze: nákupní seznam jako jediná HTML stránka, ukládání do localStorage.
