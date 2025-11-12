import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
import pandas as pd
import random

# Deine E-Mail-Konfiguration
EMAIL_ADDRESS = 'office@danapfel-digital.de'  # Deine Absender-E-Mail
EMAIL_PASSWORD = ':,30,seNDSK'     # App-Passwort für Gmail
SMTP_SERVER = 'mail.danapfel-digital.de'
SMTP_PORT = 465

# Lade Kunden-E-Mails aus CSV
def load_emails(file_path='email.csv'):
    df = pd.read_csv(file_path)
    return df['email'].tolist()  # Angenommen, Spalte heißt 'email'

# Funktion zum Versenden einer E-Mail
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
        print(f"E-Mail an {to_email} gesendet.")
    except Exception as e:
        print(f"Fehler beim Senden an {to_email}: {e}")

# Tägliche Aufgabe: 3-4 E-Mails senden
def daily_email_task():
    emails = load_emails()
    if not emails:
        print("Keine E-Mails verfügbar.")
        return
    
    # Wähle 3-4 zufällige E-Mails (oder sequentiell, je nach Bedarf)
    num_emails = random.randint(3, 4)
    selected_emails = random.sample(emails, min(num_emails, len(emails)))
    
    subject = "Dein tägliches Update"  # Passe an
    body = "Hallo,\nhier ist dein tägliches Update. Beste Grüße!"  # Passe den Inhalt an
    
    for email in selected_emails:
        send_email(email, subject, body)
        time.sleep(10)  # Warte 10 Sekunden zwischen E-Mails, um Spam-Filter zu vermeiden

# Scheduler einrichten
schedule.every().day.at("10:00").do(daily_email_task)  # Täglich um 10:00 Uhr

# Skript laufen lassen
while True:
    schedule.run_pending()
    time.sleep(60)  # Überprüfe alle 60 Sekunden
