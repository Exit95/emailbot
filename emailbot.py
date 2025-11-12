import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import random
import time

# Deine E-Mail-Konfiguration (passe an deinen Mailserver an)
EMAIL_ADDRESS = 'office@danapfel-digital.de'  # Absender
EMAIL_PASSWORD = ':,30,seNDSK'  # Falls Auth benötigt
SMTP_SERVER = 'mail.danapfel-digital.de'  # Oder IP deines Servers, z. B. 'mail.deinedomain.de'
SMTP_PORT = 25  # Oder 587 für TLS

# Lade Kunden-E-Mails aus CSV
def load_emails(file_path='email.csv'):
    try:
        df = pd.read_csv(file_path)
        return df['email'].tolist()
    except FileNotFoundError:
        print("CSV-Datei nicht gefunden! Erstelle eine mit Test-Adressen.")
        return []

# Funktion zum Versenden einer E-Mail
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        if SMTP_PORT == 587:
            server.starttls()  # TLS aktivieren, falls nötig
        if EMAIL_PASSWORD:  # Nur wenn Auth benötigt
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
        print(f"✓ E-Mail erfolgreich an {to_email} gesendet!")
    except Exception as e:
        print(f"✗ Fehler beim Senden an {to_email}: {e}")

# Test-Aufgabe: Sofort 1 E-Mail senden (für mehr: num_emails = random.randint(3,4))
def test_email_task():
    emails = load_emails()
    if not emails:
        print("Keine E-Mails in der CSV! Füge Test-Adressen hinzu.")
        return
    
    # Für Test: Nur die erste E-Mail (oder deine eigene)
    num_emails = 1  # Ändere zu random.randint(3,4) für vollen Test
    selected_emails = emails[:num_emails]  # Oder random.sample(emails, num_emails)
    
    subject = "Test-E-Mail von deinem Bot"
    body = """Hallo,

das ist eine Test-Nachricht von deinem E-Mail-Bot. Alles funktioniert!

Falls das Werbung ist: Du hast zugestimmt, oder? 😊

Beste Grüße,
Dein Unternehmen
(Abmelden: [Hier Link einfügen für Produktion])"""
    
    for email in selected_emails:
        send_email(email, subject, body)
        if num_emails > 1:
            time.sleep(10)  # Pause zwischen Sends

# Sofort ausführen
if __name__ == "__main__":
    print("Starte Test-Versand...")
    test_email_task()
    print("Test abgeschlossen!")