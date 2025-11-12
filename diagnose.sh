#!/bin/bash

# SMTP Diagnose Startskript

echo "=========================================="
echo "MAILCOW SMTP DIAGNOSE"
echo "=========================================="
echo ""

# Prüfe ob Virtual Environment existiert
if [ ! -d "venv" ]; then
    echo "Virtual Environment nicht gefunden. Erstelle venv..."
    python3 -m venv venv
    echo "Installiere Abhängigkeiten..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Starte das Diagnose-Skript
python diagnose.py

echo ""
echo "=========================================="
echo "Diagnose abgeschlossen!"
echo "=========================================="

