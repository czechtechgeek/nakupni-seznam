# 🛒 Nákupní seznam

Jednoduchý nákupní seznam jako jediná HTML stránka — bez serveru, bez databáze, bez závislostí. Data se ukládají do `localStorage` prohlížeče.

## Co umí

- Přidávání položek s množstvím a kategorií
- Rychlé přidání tlačítkem **+** (Enter funguje taky) a odebrání tlačítkem **−** u každé položky
- Odškrtávání nakoupeného, mazání, řazení
- Světlý a tmavý režim podle nastavení systému
- Funguje offline (vše je v jednom souboru)

## Použití

- **V prohlížeči:** otevři `index.html` (nebo GitHub Pages)
- **Home Assistant:** jako add-on z tohoto repozitáře — viz níže

## Instalace do Home Assistant

Repozitář je zároveň **add-on repository**:

1. HA → **Nastavení → Doplňky → Obchod s doplňky**
2. Vpravo nahoře **⋮ → Repozitáře**
3. Přidat `https://github.com/czechtechgeek/nakupni-seznam`
4. Obnovit obchod → **Nákupní seznam** → **Nainstalovat** → **Spustit**

Po startu je aplikace v postranním panelu **Nákupy**. Add-on běží na portu **8091** (ingress), takže je dostupná i přímo na `http://homeassistant.local:8091`.

## Struktura

```
index.html            vlastní aplikace (jediný soubor)
addon/                Home Assistant add-on
  config.yaml         metadata, ingress, port 8091
  Dockerfile          nginx:alpine + statické soubory
  nginx.conf          SPA fallback (funguje i s ingress prefixem)
  app/index.html      generovaná kopie (packaging/sync_addon.sh)
  icon.png, logo.png
repository.yaml       registrace repozitáře v HA
packaging/sync_addon.sh
tools/make_icons.py
```

## Vývoj

```bash
./packaging/sync_addon.sh          # zkopíruje index.html do addonu
cd addon && docker build -t nakupni-seznam . && docker run -p 8091:8091 nakupni-seznam
```

## Poznámka k datům

Seznam je uložen v prohlížeči (localStorage), takže **se nesynchronizuje mezi zařízeními**. V HA ingressu i na přímém portu jde o jiný origin — každý má vlastní seznam. Pokud budeš chtít sdílení mezi telefonem a PC, je potřeba serverová část (SQLite + API).
