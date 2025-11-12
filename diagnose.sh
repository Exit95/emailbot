#!/bin/bash

# SMTP Diagnose - Vollständiges Setup & Start-Skript
# Installiert alle Abhängigkeiten und führt Diagnose durch

set -e  # Bei Fehler abbrechen

echo "=========================================="
echo "MAILCOW SMTP DIAGNOSE - VOLLSTÄNDIG"
echo "=========================================="
echo ""

# Funktion für farbige Ausgabe
print_success() {
    echo -e "\033[0;32m✓ $1\033[0m"
}

print_error() {
    echo -e "\033[0;31m✗ $1\033[0m"
}

print_info() {
    echo -e "\033[0;34mℹ $1\033[0m"
}

# 1. System-Updates und Python-Installation prüfen
echo "[1/5] Prüfe System-Voraussetzungen..."
echo "----------------------------------------"

# Prüfe ob apt verfügbar ist (Debian/Ubuntu)
if command -v apt-get &> /dev/null; then
    print_info "Debian/Ubuntu System erkannt"

    # Prüfe ob Python3 installiert ist
    if ! command -v python3 &> /dev/null; then
        print_info "Python3 nicht gefunden. Installiere Python3..."
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv python3-full
        print_success "Python3 installiert"
    else
        print_success "Python3 ist bereits installiert: $(python3 --version)"
    fi

# Prüfe ob yum verfügbar ist (RedHat/CentOS)
elif command -v yum &> /dev/null; then
    print_info "RedHat/CentOS System erkannt"

    if ! command -v python3 &> /dev/null; then
        print_info "Python3 nicht gefunden. Installiere Python3..."
        sudo yum install -y python3 python3-pip
        print_success "Python3 installiert"
    else
        print_success "Python3 ist bereits installiert: $(python3 --version)"
    fi

else
    print_info "Unbekanntes System. Überspringe Paket-Installation."
    print_info "Stelle sicher, dass Python3 installiert ist!"
fi

echo ""

# 2. Prüfe Python-Version
echo "[2/5] Prüfe Python-Version..."
echo "----------------------------------------"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python Version: $PYTHON_VERSION"
echo ""

# 3. Virtual Environment erstellen/aktivieren
echo "[3/5] Virtual Environment Setup..."
echo "----------------------------------------"
if [ ! -d "venv" ]; then
    print_info "Virtual Environment nicht gefunden. Erstelle venv..."
    python3 -m venv venv
    print_success "Virtual Environment erstellt"
else
    print_success "Virtual Environment existiert bereits"
fi

# Virtual Environment aktivieren
source venv/bin/activate
print_success "Virtual Environment aktiviert"
echo ""

# 4. Pip upgraden
echo "[4/5] Upgrade pip..."
echo "----------------------------------------"
pip install --upgrade pip > /dev/null 2>&1
print_success "pip aktualisiert: $(pip --version)"
echo ""

# 5. Abhängigkeiten installieren (für Diagnose nicht nötig, aber für Konsistenz)
echo "[5/5] Prüfe Python-Abhängigkeiten..."
echo "----------------------------------------"
print_success "Keine zusätzlichen Pakete für Diagnose nötig"
echo ""

# Starte das Diagnose-Skript
echo "=========================================="
echo "STARTE SMTP DIAGNOSE"
echo "=========================================="
echo ""

python diagnose.py

# Deaktiviere Virtual Environment nach Ausführung
deactivate 2>/dev/null || true

echo ""
echo "=========================================="
print_success "Diagnose abgeschlossen!"
echo "=========================================="

