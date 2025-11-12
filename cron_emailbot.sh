#!/bin/bash

# Cronjob-Skript für automatischen E-Mail-Versand
# Wird täglich um 08:00 Uhr ausgeführt

# Wechsle ins Projektverzeichnis
cd /root/emailbot || exit 1

# Logfile mit Datum
LOG_DIR="/root/emailbot/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/emailbot_$(date +%Y-%m-%d).log"

# Starte Logging
echo "========================================" >> "$LOG_FILE"
echo "E-Mail Bot gestartet: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Aktiviere Virtual Environment und führe Script aus
source venv/bin/activate >> "$LOG_FILE" 2>&1

# Führe E-Mail-Bot aus
./venv/bin/python3 emailbot.py >> "$LOG_FILE" 2>&1

# Exit Code speichern
EXIT_CODE=$?

# Deaktiviere Virtual Environment
deactivate 2>/dev/null || true

# Abschluss-Log
echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "E-Mail Bot beendet: $(date)" >> "$LOG_FILE"
echo "Exit Code: $EXIT_CODE" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Alte Logs löschen (älter als 30 Tage)
find "$LOG_DIR" -name "emailbot_*.log" -mtime +30 -delete

exit $EXIT_CODE

