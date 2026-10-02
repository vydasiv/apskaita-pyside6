#!/bin/bash
# Kubuntu 24.04 / 26.04 LTS paleidimo skriptas
set -e
cd "$(dirname "$0")"

echo "=== Tikrinama Python aplinka ==="
if [ ! -d "venv" ]; then
    echo "Kuriama virtuali aplinka (PEP 668 suderinamumas)..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Diegiamos priklausomybės..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "Paleidžiama programa..."
python3 main.py
