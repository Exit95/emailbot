#!/bin/bash

# E-Mail Bot Vollständiges Setup & Start-Skript
# Installiert alle Abhängigkeiten und startet den Bot

set -e  # Bei Fehler abbrechen

echo "=========================================="
echo "E-MAIL BOT - VOLLSTÄNDIGE INSTALLATION"
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
echo "[1/6] Prüfe System-Voraussetzungen..."
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

    # Prüfe ob git installiert ist
    if ! command -v git &> /dev/null; then
        print_info "Git nicht gefunden. Installiere Git..."
        sudo apt-get install -y git
        print_success "Git installiert"
    else
        print_success "Git ist bereits installiert"
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

    if ! command -v git &> /dev/null; then
        print_info "Git nicht gefunden. Installiere Git..."
        sudo yum install -y git
        print_success "Git installiert"
    else
        print_success "Git ist bereits installiert"
    fi

else
    print_info "Unbekanntes System. Überspringe Paket-Installation."
    print_info "Stelle sicher, dass Python3 und Git installiert sind!"
fi

echo ""

# 2. Prüfe Python-Version
echo "[2/6] Prüfe Python-Version..."
echo "----------------------------------------"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python Version: $PYTHON_VERSION"
echo ""

# 3. Virtual Environment erstellen/aktivieren
echo "[3/6] Virtual Environment Setup..."
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
echo "[4/6] Upgrade pip..."
echo "----------------------------------------"
pip install --upgrade pip > /dev/null 2>&1
print_success "pip aktualisiert: $(pip --version)"
echo ""

# 5. Abhängigkeiten installieren
echo "[5/6] Installiere Python-Abhängigkeiten..."
echo "----------------------------------------"
if [ -f "requirements.txt" ]; then
    print_info "Installiere Pakete aus requirements.txt..."
    pip install -r requirements.txt
    print_success "Alle Abhängigkeiten installiert"
else
    print_info "requirements.txt nicht gefunden. Installiere pandas direkt..."
    pip install pandas
    print_success "pandas installiert"
fi
echo ""

# 6. Prüfe ob email.csv existiert
echo "[6/6] Prüfe Konfiguration..."
echo "----------------------------------------"
if [ ! -f "email.csv" ]; then
    print_error "email.csv nicht gefunden!"
    print_info "Erstelle Beispiel email.csv..."
    echo "email" > email.csv
    echo "test@example.com" >> email.csv
    print_success "Beispiel email.csv erstellt"
    print_info "Bitte bearbeiten Sie email.csv und fügen Sie echte E-Mail-Adressen hinzu!"
else
    EMAIL_COUNT=$(tail -n +2 email.csv | wc -l)
    print_success "email.csv gefunden mit $EMAIL_COUNT E-Mail-Adresse(n)"
fi
echo ""

# 7. Starte den E-Mail Bot
echo "=========================================="
echo "STARTE E-MAIL BOT"
echo "=========================================="
echo ""

python emailbot.py

# Deaktiviere Virtual Environment nach Ausführung
deactivate 2>/dev/null || true

echo ""
echo "=========================================="
print_success "E-Mail Bot beendet"
echo "=========================================="
