#!/bin/sh
# Zkopíruje aplikaci a backend z kořene repa do add-on buildu.
set -e
cd "$(dirname "$0")/.."
mkdir -p addon/src/static
cp index.html addon/src/static/index.html
cp backend/app.py addon/src/app.py
cp backend/requirements.txt addon/src/requirements.txt
echo "addon/src: index.html $(wc -c < addon/src/static/index.html) B, app.py $(wc -c < addon/src/app.py) B"
