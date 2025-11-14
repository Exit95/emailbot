#!/bin/bash

# Wrapper-Skript für 2-wöchentlichen E-Mail-Versand
# Wird jeden Montag um 08:00 Uhr aufgerufen, führt aber nur alle 2 Wochen aus

# Wechsle ins Projektverzeichnis
cd /root/emailbot || exit 1

# Datei zum Speichern des letzten Ausführungsdatums
LAST_RUN_FILE="/root/emailbot/.last_run"

# Aktuelles Datum (Sekunden seit Epoch)
CURRENT_DATE=$(date +%s)

# Prüfe ob Datei existiert
if [ -f "$LAST_RUN_FILE" ]; then
    # Lese letztes Ausführungsdatum
    LAST_RUN=$(cat "$LAST_RUN_FILE")
    
    # Berechne Differenz in Tagen
    DIFF_SECONDS=$((CURRENT_DATE - LAST_RUN))
    DIFF_DAYS=$((DIFF_SECONDS / 86400))
    
    # Wenn weniger als 13 Tage vergangen sind, überspringe
    if [ $DIFF_DAYS -lt 13 ]; then
        echo "Letzter Versand vor $DIFF_DAYS Tagen. Überspringe (nächster Versand in $((14 - DIFF_DAYS)) Tagen)."
        exit 0
    fi
fi

# Speichere aktuelles Datum
echo "$CURRENT_DATE" > "$LAST_RUN_FILE"

# Führe E-Mail-Bot aus
/usr/bin/python3 /root/emailbot/emailbot.py

exit $?

