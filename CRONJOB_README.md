# 🤖 E-Mail Bot - Automatischer Versand

## 📋 Übersicht

Der E-Mail Bot versendet **Montags und Donnerstags um 08:00 Uhr** automatisch E-Mails an alle Adressen in `email.csv`.

**Zwei Methoden verfügbar:**
- ✅ **systemd Timer** (empfohlen für moderne Linux-Systeme)
- ✅ **Cronjob** (klassische Methode)

---

## 🚀 Installation

### Methode 1: systemd Timer (EMPFOHLEN)

```bash
cd /root/emailbot
chmod +x setup_systemd.sh
./setup_systemd.sh
```

Das Skript:
- ✅ Installiert systemd Service und Timer
- ✅ Richtet den Timer ein (Montag & Donnerstag um 08:00 Uhr)
- ✅ Erstellt das Logs-Verzeichnis
- ✅ Bietet einen Testlauf an
- ✅ Startet automatisch beim Booten

### Methode 2: Cronjob (Klassisch)

```bash
cd /root/emailbot
chmod +x setup_cronjob.sh
./setup_cronjob.sh
```

Das Skript:
- ✅ Richtet den Cronjob ein (Montag & Donnerstag um 08:00 Uhr)
- ✅ Erstellt das Logs-Verzeichnis
- ✅ Bietet einen Testlauf an

### 2. E-Mail-Adressen hinzufügen

Bearbeiten Sie `email.csv`:

```bash
nano email.csv
```

Fügen Sie E-Mail-Adressen hinzu (eine pro Zeile):

```csv
email
kunde1@example.com
kunde2@example.com
kunde3@example.com
```

---

## 📊 Verwaltung

### systemd Timer (wenn installiert)

**Timer-Status anzeigen:**
```bash
systemctl status emailbot.timer
```

**Nächste Ausführungen anzeigen:**
```bash
systemctl list-timers emailbot.timer
```

**Timer stoppen:**
```bash
systemctl stop emailbot.timer
```

**Timer deaktivieren:**
```bash
systemctl disable emailbot.timer
```

**Manueller Versand (sofort):**
```bash
systemctl start emailbot.service
```

**Logs anzeigen (systemd):**
```bash
journalctl -u emailbot.service -f
```

---

### Cronjob (wenn installiert)

**Cronjob anzeigen:**
```bash
crontab -l
```

**Cronjob bearbeiten:**
```bash
crontab -e
```

**Cronjob entfernen:**
```bash
crontab -e
# Dann die Zeile mit "cron_emailbot.sh" löschen
```

**Manueller Versand (sofort):**
```bash
cd /root/emailbot
./cron_emailbot.sh
```

---

## 📁 Logs

### Logs anzeigen (Live)

```bash
tail -f ~/emailbot/logs/emailbot_$(date +%Y-%m-%d).log
```

### Alle Logs anzeigen

```bash
ls -lh ~/emailbot/logs/
```

### Logs löschen (älter als 30 Tage)

Wird automatisch vom Cronjob erledigt!

---

## ⏰ Zeitplan ändern

Bearbeiten Sie den Cronjob:

```bash
crontab -e
```

**Beispiele:**

| Zeit | Cronjob-Syntax |
|------|----------------|
| Täglich um 08:00 Uhr | `0 8 * * *` |
| Täglich um 09:30 Uhr | `30 9 * * *` |
| Montag-Freitag um 08:00 Uhr | `0 8 * * 1-5` |
| Jeden Montag um 10:00 Uhr | `0 10 * * 1` |
| Alle 2 Stunden | `0 */2 * * *` |

---

## 🔧 Troubleshooting

### Cronjob läuft nicht?

1. **Prüfe ob Cronjob installiert ist:**
   ```bash
   crontab -l | grep emailbot
   ```

2. **Prüfe Logs:**
   ```bash
   tail -50 ~/emailbot/logs/emailbot_$(date +%Y-%m-%d).log
   ```

3. **Teste manuell:**
   ```bash
   cd ~/emailbot
   ./cron_emailbot.sh
   ```

### E-Mails werden nicht versendet?

1. **Prüfe email.csv:**
   ```bash
   cat ~/emailbot/email.csv
   ```

2. **Teste SMTP-Verbindung:**
   ```bash
   cd ~/emailbot
   source venv/bin/activate
   python3 diagnose.py
   ```

3. **Prüfe Mailcow:**
   ```bash
   docker ps | grep mailcow
   ```

---

## 📧 E-Mail-Inhalt ändern

Bearbeiten Sie `emailbot.py`:

```bash
nano ~/emailbot/emailbot.py
```

Suchen Sie nach:
```python
subject = "Ihre Website verdient mehr..."
body = """Sehr geehrte Damen und Herren,..."""
```

Ändern Sie den Text und speichern Sie mit `Ctrl+O` → `Enter` → `Ctrl+X`.

Dann:
```bash
git add emailbot.py
git commit -m "E-Mail-Text aktualisiert"
git push
```

---

## 🎯 Nützliche Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `./setup_cronjob.sh` | Cronjob installieren |
| `./cron_emailbot.sh` | Manueller Versand |
| `crontab -l` | Cronjob anzeigen |
| `crontab -e` | Cronjob bearbeiten |
| `tail -f logs/emailbot_*.log` | Logs live anzeigen |
| `nano email.csv` | E-Mail-Adressen bearbeiten |

---

## ✅ Checkliste

- [ ] Cronjob installiert (`./setup_cronjob.sh`)
- [ ] E-Mail-Adressen in `email.csv` eingetragen
- [ ] Testlauf erfolgreich durchgeführt
- [ ] Logs-Verzeichnis erstellt
- [ ] Erste E-Mails versendet

---

## 📞 Support

Bei Problemen:
1. Prüfe Logs: `tail -f logs/emailbot_*.log`
2. Teste manuell: `./cron_emailbot.sh`
3. Prüfe Cronjob: `crontab -l`

---

**Viel Erfolg mit dem automatischen E-Mail-Versand! 🚀**

