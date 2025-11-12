import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import random
import time
import socket

# Mailcow Server Konfiguration
EMAIL_ADDRESS = 'office@danapfel-digital.de'  # Absender-E-Mail
EMAIL_PASSWORD = ':,30,seNDSK'  # Mailbox-Passwort
SMTP_SERVER = 'mail.danapfel-digital.de'  # Mailcow SMTP Server
SMTP_PORT = 465  # Port 465 für SSL/TLS (Alternative: 587 für STARTTLS)
USE_SSL = True  # True für Port 465, False für Port 587

# Lade Kunden-E-Mails aus CSV
def load_emails(file_path='email.csv'):
    try:
        df = pd.read_csv(file_path)
        return df['email'].tolist()
    except FileNotFoundError:
        print("CSV-Datei nicht gefunden! Erstelle eine mit Test-Adressen.")
        return []

# Funktion zum Versenden einer E-Mail über Mailcow
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Verbindung zum Mailcow SMTP Server
        print(f"Verbinde mit {SMTP_SERVER}:{SMTP_PORT}...")

        # IPv4 erzwingen (IPv6 kann Probleme machen)
        old_getaddrinfo = socket.getaddrinfo
        def getaddrinfo_ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
            return old_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
        socket.getaddrinfo = getaddrinfo_ipv4_only

        if USE_SSL:
            # SSL/TLS Verbindung (Port 465)
            print("Verwende SSL/TLS Verbindung (IPv4)...")
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30)
            # server.set_debuglevel(1)  # Für Debugging auskommentieren
            server.ehlo()
        else:
            # STARTTLS Verbindung (Port 587)
            print("Verwende STARTTLS Verbindung (IPv4)...")
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
            # server.set_debuglevel(1)  # Für Debugging auskommentieren
            server.ehlo()
            server.starttls()
            server.ehlo()

        # Socket-Funktion wiederherstellen
        socket.getaddrinfo = old_getaddrinfo

        # Login mit Mailcow-Credentials
        print(f"Login als {EMAIL_ADDRESS}...")
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # E-Mail versenden
        print(f"Sende E-Mail an {to_email}...")
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
        print(f"✓ E-Mail erfolgreich an {to_email} gesendet!")
        return True
    except Exception as e:
        print(f"✗ Fehler beim Senden an {to_email}: {e}")
        import traceback
        traceback.print_exc()
        return False

# E-Mail-Versand an alle Adressen in der CSV
def send_bulk_emails():
    emails = load_emails()
    if not emails:
        print("Keine E-Mails in der CSV! Füge Test-Adressen hinzu.")
        return

    print(f"\n{len(emails)} E-Mail-Adresse(n) gefunden in email.csv")
    print("=" * 60)

    subject = "Test-E-Mail von Danapfel Digital"
    body = """Hallo,

das ist eine Test-Nachricht von deinem E-Mail-Bot über Mailcow.
Alles funktioniert einwandfrei!

Beste Grüße,
Danapfel Digital Team

---
Falls Sie diese E-Mail nicht erhalten möchten, antworten Sie bitte mit "Abmelden"."""

    successful = 0
    failed = 0

    for i, email in enumerate(emails, 1):
        print(f"\n[{i}/{len(emails)}] Sende an: {email}")
        print("-" * 60)

        if send_email(email, subject, body):
            successful += 1
        else:
            failed += 1

        # Pause zwischen E-Mails (außer bei der letzten)
        if i < len(emails):
            wait_time = 5
            print(f"Warte {wait_time} Sekunden bis zur nächsten E-Mail...")
            time.sleep(wait_time)

    print("\n" + "=" * 60)
    print(f"Versand abgeschlossen!")
    print(f"✓ Erfolgreich: {successful}")
    print(f"✗ Fehlgeschlagen: {failed}")
    print("=" * 60)

# Programm starten
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("E-MAIL BOT - Mailcow SMTP Versand")
    print("=" * 60)
    print(f"SMTP Server: {SMTP_SERVER}:{SMTP_PORT}")
    print(f"Verbindungstyp: {'SSL/TLS' if USE_SSL else 'STARTTLS'}")
    print(f"Absender: {EMAIL_ADDRESS}")
    print("=" * 60)

    send_bulk_emails()