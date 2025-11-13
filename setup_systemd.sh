#!/bin/bash

# Setup-Skript für systemd Timer Installation
# Richtet den automatischen E-Mail-Versand Montags und Donnerstags um 08:00 Uhr ein

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
echo "  SYSTEMD TIMER SETUP - E-Mail Bot"
echo "=========================================="
echo ""

# Prüfe ob wir root sind
if [ "$EUID" -ne 0 ]; then
    print_error "Dieses Skript muss als root ausgeführt werden!"
    print_info "Verwenden Sie: sudo ./setup_systemd.sh"
    exit 1
fi

# Prüfe ob wir im richtigen Verzeichnis sind
if [ ! -f "emailbot.py" ]; then
    print_error "emailbot.py nicht gefunden!"
    print_info "Bitte führen Sie dieses Skript im emailbot-Verzeichnis aus."
    exit 1
fi

# Erstelle Logs-Verzeichnis
print_info "Erstelle Logs-Verzeichnis..."
mkdir -p /root/emailbot/logs
print_success "Logs-Verzeichnis erstellt"
echo ""

# Mache Cronjob-Skript ausführbar
print_info "Mache cron_emailbot.sh ausführbar..."
chmod +x /root/emailbot/cron_emailbot.sh
print_success "cron_emailbot.sh ist ausführbar"
echo ""

# Kopiere systemd-Dateien
print_info "Installiere systemd Service und Timer..."

# Service-Datei kopieren
cp emailbot.service /etc/systemd/system/
print_success "emailbot.service installiert"

# Timer-Datei kopieren
cp emailbot.timer /etc/systemd/system/
print_success "emailbot.timer installiert"
echo ""

# Systemd neu laden
print_info "Lade systemd-Konfiguration neu..."
systemctl daemon-reload
print_success "systemd neu geladen"
echo ""

# Prüfe ob Timer bereits läuft
if systemctl is-enabled emailbot.timer &>/dev/null; then
    print_warning "Timer ist bereits aktiviert!"
    print_info "Stoppe und deaktiviere alten Timer..."
    systemctl stop emailbot.timer
    systemctl disable emailbot.timer
    echo ""
fi

# Aktiviere und starte Timer
print_info "Aktiviere E-Mail Bot Timer..."
systemctl enable emailbot.timer
print_success "Timer aktiviert (startet automatisch beim Booten)"
echo ""

print_info "Starte Timer..."
systemctl start emailbot.timer
print_success "Timer gestartet"
echo ""

# Zeige Status
echo "=========================================="
echo "  TIMER STATUS"
echo "=========================================="
echo ""
systemctl status emailbot.timer --no-pager -l
echo ""

# Zeige nächste Ausführungszeiten
echo "=========================================="
echo "  NÄCHSTE AUSFÜHRUNGEN"
echo "=========================================="
echo ""
systemctl list-timers emailbot.timer --no-pager
echo ""

# Zeige Konfiguration
echo "=========================================="
echo "  KONFIGURATION"
echo "=========================================="
echo ""
print_info "Zeitplan: Alle 2 Wochen Montags um 08:00 Uhr"
print_info "Service: /etc/systemd/system/emailbot.service"
print_info "Timer: /etc/systemd/system/emailbot.timer"
print_info "Skript: /root/emailbot/cron_emailbot.sh"
print_info "Logs: /root/emailbot/logs/"
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
    systemctl start emailbot.service
    echo ""
    print_info "Warte auf Abschluss..."
    sleep 2
    echo ""
    systemctl status emailbot.service --no-pager -l
    echo ""
    print_success "Testlauf abgeschlossen!"
    print_info "Log-Datei: /root/emailbot/logs/emailbot_$(date +%Y-%m-%d).log"
else
    print_info "Testlauf übersprungen."
fi

echo ""
echo "=========================================="
echo "  SETUP ABGESCHLOSSEN"
echo "=========================================="
echo ""
print_success "systemd Timer erfolgreich eingerichtet!"
print_info "E-Mails werden ab jetzt alle 2 Wochen Montags um 08:00 Uhr versendet."
echo ""
print_info "Nützliche Befehle:"
echo "  • Timer-Status:        systemctl status emailbot.timer"
echo "  • Nächste Ausführung:  systemctl list-timers emailbot.timer"
echo "  • Timer stoppen:       systemctl stop emailbot.timer"
echo "  • Timer deaktivieren:  systemctl disable emailbot.timer"
echo "  • Manueller Versand:   systemctl start emailbot.service"
echo "  • Logs anzeigen:       journalctl -u emailbot.service -f"
echo "  • Datei-Logs:          tail -f /root/emailbot/logs/emailbot_*.log"
echo ""

