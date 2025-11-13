#!/bin/bash

# Setup-Skript für Cronjob-Installation
# Richtet den automatischen E-Mail-Versand um 08:00 Uhr ein

# Farben für Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo ""
echo "=========================================="
echo "  CRONJOB SETUP - E-Mail Bot"
echo "=========================================="
echo ""

# Prüfe ob wir im richtigen Verzeichnis sind
if [ ! -f "emailbot.py" ]; then
    print_error "emailbot.py nicht gefunden!"
    print_info "Bitte führen Sie dieses Skript im emailbot-Verzeichnis aus."
    exit 1
fi

# Mache Cronjob-Skript ausführbar
print_info "Mache cron_emailbot.sh ausführbar..."
chmod +x cron_emailbot.sh
print_success "cron_emailbot.sh ist jetzt ausführbar"
echo ""

# Erstelle Logs-Verzeichnis
print_info "Erstelle Logs-Verzeichnis..."
mkdir -p logs
print_success "Logs-Verzeichnis erstellt: $(pwd)/logs"
echo ""

# Prüfe ob Cronjob bereits existiert
# Montag = 1, Donnerstag = 4
CRON_ENTRY="0 8 * * 1,4 /root/emailbot/cron_emailbot.sh"
EXISTING_CRON=$(crontab -l 2>/dev/null | grep -F "cron_emailbot.sh" || true)

if [ -n "$EXISTING_CRON" ]; then
    print_warning "Cronjob existiert bereits!"
    echo "Aktueller Eintrag:"
    echo "  $EXISTING_CRON"
    echo ""
    read -p "Möchten Sie den Cronjob neu installieren? (j/n): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[JjYy]$ ]]; then
        print_info "Installation abgebrochen."
        exit 0
    fi
    
    # Entferne alten Cronjob
    print_info "Entferne alten Cronjob..."
    (crontab -l 2>/dev/null | grep -v "cron_emailbot.sh") | crontab -
    print_success "Alter Cronjob entfernt"
    echo ""
fi

# Installiere neuen Cronjob
print_info "Installiere Cronjob für täglichen Versand um 08:00 Uhr..."
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
print_success "Cronjob erfolgreich installiert!"
echo ""

# Zeige aktuellen Cronjob
echo "=========================================="
echo "  CRONJOB KONFIGURATION"
echo "=========================================="
echo ""
print_info "Aktueller Cronjob:"
crontab -l | grep "cron_emailbot.sh"
echo ""
print_info "Zeitplan: Montags und Donnerstags um 08:00 Uhr"
print_info "Skript: /root/emailbot/cron_emailbot.sh"
print_info "Logs: /root/emailbot/logs/"
echo ""

# Zeige nächste Ausführungszeit
echo "=========================================="
echo "  NÄCHSTE AUSFÜHRUNG"
echo "=========================================="
echo ""
CURRENT_TIME=$(date +"%H:%M")
CURRENT_DAY=$(date +"%u")  # 1=Montag, 4=Donnerstag

# Berechne nächsten Versand-Tag
if [ "$CURRENT_DAY" -eq 1 ] && [ "$(date +%H)" -lt 8 ]; then
    NEXT_RUN="Heute (Montag) um 08:00 Uhr"
elif [ "$CURRENT_DAY" -eq 4 ] && [ "$(date +%H)" -lt 8 ]; then
    NEXT_RUN="Heute (Donnerstag) um 08:00 Uhr"
elif [ "$CURRENT_DAY" -lt 4 ]; then
    NEXT_RUN="Donnerstag um 08:00 Uhr"
else
    NEXT_RUN="Nächsten Montag um 08:00 Uhr"
fi

print_info "Aktuelle Zeit: $CURRENT_TIME ($(date +%A))"
print_success "Nächster automatischer Versand: $NEXT_RUN"
echo ""

# Testlauf anbieten
echo "=========================================="
echo "  TESTLAUF"
echo "=========================================="
echo ""
print_warning "Möchten Sie einen Testlauf durchführen?"
print_info "Dies sendet E-Mails an alle Adressen in email.csv"
echo ""
read -p "Testlauf jetzt starten? (j/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[JjYy]$ ]]; then
    print_info "Starte Testlauf..."
    echo ""
    ./cron_emailbot.sh
    echo ""
    print_success "Testlauf abgeschlossen!"
    print_info "Log-Datei: logs/emailbot_$(date +%Y-%m-%d).log"
else
    print_info "Testlauf übersprungen."
fi

echo ""
echo "=========================================="
echo "  SETUP ABGESCHLOSSEN"
echo "=========================================="
echo ""
print_success "Cronjob erfolgreich eingerichtet!"
print_info "E-Mails werden ab jetzt Montags und Donnerstags um 08:00 Uhr versendet."
echo ""
print_info "Nützliche Befehle:"
echo "  • Cronjob anzeigen:    crontab -l"
echo "  • Cronjob entfernen:   crontab -e  (dann Zeile löschen)"
echo "  • Logs anzeigen:       tail -f logs/emailbot_$(date +%Y-%m-%d).log"
echo "  • Manueller Versand:   ./cron_emailbot.sh"
echo ""

