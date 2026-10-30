#!/bin/sh
# Zkopíruje aplikaci z kořene repa do add-on buildu.
set -e
cd "$(dirname "$0")/.."
mkdir -p addon/app
cp index.html addon/app/index.html
echo "addon/app/index.html: $(wc -c < addon/app/index.html) bytes"
