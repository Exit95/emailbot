import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import random
import time
import socket
import os

# Mailcow Server Konfiguration
EMAIL_ADDRESS = 'office@danapfel-digital.de'  # Absender-E-Mail
EMAIL_PASSWORD = ':,30,seNDSK'  # Mailbox-Passwort
EMAIL_DISPLAY_NAME = 'Michael Danapfel - Danapfel Digital'  # Anzeigename

# Auto-Erkennung: Wenn auf Mailcow-VM, verwende localhost
# Prüfe ob Docker mit Mailcow läuft
def detect_smtp_server():
    try:
        # Prüfe ob wir auf dem Mailcow-Server sind
        result = os.popen('docker ps 2>/dev/null | grep -i mailcow').read()
        if 'mailcow' in result.lower():
            print("✓ Mailcow Docker erkannt - verwende localhost")
            return 'localhost'
    except:
        pass

    # Fallback: Verwende externen Server
    return 'mail.danapfel-digital.de'

SMTP_SERVER = detect_smtp_server()  # Auto-Erkennung
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
    # Setze Absender mit Anzeigenamen
    msg['From'] = f'"{EMAIL_DISPLAY_NAME}" <{EMAIL_ADDRESS}>'
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

    subject = "Ihre Website verdient mehr – modern, schnell und professionell mit Danapfel Digital"
    body = """Sehr geehrte Damen und Herren,

viele Unternehmen haben heute dasselbe Problem:
Die Website wirkt veraltet, lädt langsam oder bringt kaum Anfragen. Dabei ist genau sie oft der erste Eindruck, den Kunden bekommen.

Hier kommt Danapfel Digital ins Spiel.
Wir entwickeln moderne, suchmaschinenoptimierte Webseiten, die nicht nur gut aussehen, sondern auch verkaufen. Ob Sie eine neue Website brauchen oder einfach nur zu uns wechseln möchten, beides ist möglich. Wir kümmern uns um Design, Technik, Hosting und alles, was dazu gehört.

Unsere Leistungen im Überblick:

• Erstellung moderner Business-Webseiten und One-Pager
• Komplette Betreuung inkl. Hosting, Domain & SSL
• Wartung, Updates und technischer Support
• Optional: SEO, Social Media & Online-Werbung
• und noch vieles mehr!

Wir arbeiten transparent, fair und ohne lange Verträge, ideal für lokale Unternehmen, die Wert auf Qualität und direkten Kontakt legen.

Wenn Sie möchten, schaue ich mir Ihre aktuelle Website unverbindlich an und zeige Ihnen, wie wir sie optimieren oder neu aufsetzen können.

Wann passt es Ihnen für ein kurzes Gespräch?

Viele Grüße
Michael Danapfel
Danapfel Digital
https://danapfel-digital.de"""

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