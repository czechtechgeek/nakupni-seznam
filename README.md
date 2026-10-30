# 🛒 Nákupní seznam

Nákupní seznam do prohlížeče i do Home Assistantu. Jako add-on drží data na serveru, takže **seznam vidí všichni uživatelé HA**; samotná stránka funguje i offline díky `localStorage` jako záloze.

## Co umí

- Přidávání položek s množstvím a kategorií
- Rychlé přidání tlačítkem **+** (Enter funguje taky) a odebrání tlačítkem **−** u každé položky
- Odškrtávání nakoupeného, mazání, řazení
- Světlý a tmavý režim podle nastavení systému
- Funguje offline (stav se ukládá i do `localStorage`)

## Použití

- **V prohlížeči:** otevři `index.html` (nebo GitHub Pages)
- **Home Assistant:** jako add-on z tohoto repozitáře — společný seznam pro všechny uživatele, viz níže

## Instalace do Home Assistant

Repozitář je zároveň **add-on repository**:

1. HA → **Nastavení → Doplňky → Obchod s doplňky**
2. Vpravo nahoře **⋮ → Repozitáře**
3. Přidat `https://github.com/czechtechgeek/nakupni-seznam`
4. Obnovit obchod → **Nákupní seznam** → **Nainstalovat** → **Spustit**

Po startu je aplikace v postranním panelu **Nákupy** a je dostupná i přímo na `http://homeassistant.local:8091`.

### Sdílení mezi uživateli

Add-on ukládá seznamy do SQLite v `/data/nakupni.db`. Všichni uživatelé HA (i různé prohlížeče a telefony) tedy vidí **stejné seznamy** a změny se projeví do 5 sekund. Data přežijí restart i update add-onu.

API:

```http
GET /api/state              → {"version": 3, "data": {...}, "updatedBy": "jan"}
PUT /api/state              {"data": {...}, "base": 3} → 200, nebo 409 při konfliktu
GET /healthz                → {"ok": true, "version": 3}
```

## Struktura

```
index.html            vlastní aplikace (jediný soubor, localStorage + sync)
backend/app.py        Flask API + SQLite (jen pro add-on)
backend/requirements.txt
addon/                Home Assistant add-on
  config.yaml         metadata, ingress, port 8091
  Dockerfile          python:3.12-alpine
  run.sh              spuštění, DB v /data
  src/                generováno (packaging/sync_addon.sh)
  icon.png, logo.png
repository.yaml       registrace repozitáře v HA
packaging/sync_addon.sh
tools/make_icons.py
```

## Vývoj

```bash
./packaging/sync_addon.sh          # zkopíruje index.html + backend do addonu
cd addon && docker build -t nakupni-seznam . \
  && docker run -p 8091:8091 -v /tmp/nakupni-data:/data nakupni-seznam
```

## Poznámka k datům

- **Add-on:** data jsou v `/data/nakupni.db`, společná pro všechny uživatele HA.
- **Statická verze (GitHub Pages):** data jen v `localStorage` prohlížeče, bez sdílení.
- Při konfliktu (dva lidé upravují současně) vyhraje novější verze seznamu podle `updatedAt`; smazané seznamy se nevrátí (tombstones).
