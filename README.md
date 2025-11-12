# E-Mail Bot für Mailcow

Ein Python-basierter E-Mail-Bot zum Versenden von Bulk-E-Mails über einen Mailcow-Server.

## 🚀 Features

- ✅ SSL/TLS Verbindung (Port 465) für sichere Übertragung
- ✅ Bulk-Versand an mehrere Empfänger aus CSV-Datei
- ✅ Detaillierte Debug-Ausgaben
- ✅ Fehlerbehandlung und Statistiken
- ✅ Automatische Pausen zwischen E-Mails

## 📋 Voraussetzungen

- Python 3.7+
- Mailcow Server mit SMTP-Zugang
- Gültige E-Mail-Credentials

## 🔧 Installation

1. Repository klonen:
```bash
git clone https://github.com/Exit95/emailbot.git
cd emailbot
```

2. Virtual Environment erstellen:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

## ⚙️ Konfiguration

### E-Mail-Server Einstellungen

Bearbeiten Sie `emailbot.py` und passen Sie folgende Zeilen an:

```python
EMAIL_ADDRESS = 'ihre-email@domain.de'
EMAIL_PASSWORD = 'ihr-passwort'
SMTP_SERVER = 'mail.ihre-domain.de'
SMTP_PORT = 465  # 465 für SSL/TLS oder 587 für STARTTLS
USE_SSL = True   # True für Port 465, False für Port 587
```

### E-Mail-Empfänger

Bearbeiten Sie `email.csv` und fügen Sie E-Mail-Adressen hinzu:

```csv
email
empfaenger1@example.com
empfaenger2@example.com
empfaenger3@example.com
```

## 🎯 Verwendung

E-Mails versenden:
```bash
source venv/bin/activate
python emailbot.py
```

## 📊 Ausgabe

Das Skript zeigt detaillierte Informationen:
- Anzahl der zu versendenden E-Mails
- Verbindungsstatus zum SMTP-Server
- Authentifizierungsstatus
- Versandstatus für jede E-Mail
- Abschließende Statistik (Erfolgreich/Fehlgeschlagen)

## 🔒 Sicherheit

⚠️ **Wichtig:** 
- Committen Sie niemals Passwörter in Git!
- Verwenden Sie Umgebungsvariablen für sensible Daten in Produktion
- Die aktuelle Konfiguration ist nur für Entwicklung/Tests

## 📝 E-Mail-Inhalt anpassen

Bearbeiten Sie in `emailbot.py` die Funktion `send_bulk_emails()`:

```python
subject = "Ihr Betreff"
body = """Ihr E-Mail-Text hier..."""
```

## 🛠️ Troubleshooting

### Port 465 funktioniert nicht
Versuchen Sie Port 587 mit STARTTLS:
```python
SMTP_PORT = 587
USE_SSL = False
```

### Authentifizierung schlägt fehl
- Überprüfen Sie E-Mail-Adresse und Passwort
- Stellen Sie sicher, dass SMTP-Auth auf dem Mailcow-Server aktiviert ist

### Verbindung wird abgelehnt
- Prüfen Sie Firewall-Einstellungen
- Stellen Sie sicher, dass der SMTP-Port erreichbar ist

## 📄 Lizenz

Dieses Projekt ist für den persönlichen Gebrauch bestimmt.

## 👤 Autor

Danapfel Digital

