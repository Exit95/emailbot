import 'dotenv/config';
import nodemailer from 'nodemailer';
import { CronJob } from 'cron';
import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const STATE_FILE = path.join(__dirname, 'state.json');
const EMAILS_FILE = path.join(__dirname, 'email.json');
const TEXTS_DIR = path.join(__dirname, 'texts');

// SMTP-Transporter erstellen
const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT || '587'),
    secure: false, // true für Port 465, false für andere Ports
    auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS
    },
    tls: {
        rejectUnauthorized: false // Für self-signed certificates
    }
});

// State laden oder initialisieren
async function loadState() {
    try {
        if (await fs.pathExists(STATE_FILE)) {
            return await fs.readJson(STATE_FILE);
        }
    } catch (error) {
        console.error('Fehler beim Laden des States:', error);
    }
    return { lastTextIndex: 0, lastEmailIndex: 0 };
}

// State speichern
async function saveState(state) {
    try {
        await fs.writeJson(STATE_FILE, state, { spaces: 2 });
    } catch (error) {
        console.error('Fehler beim Speichern des States:', error);
    }
}

// E-Mails laden
async function loadEmails() {
    try {
        return await fs.readJson(EMAILS_FILE);
    } catch (error) {
        console.error('Fehler beim Laden der E-Mails:', error);
        return [];
    }
}

// Text aus Datei laden
async function loadText(textNumber) {
    try {
        const textFile = path.join(TEXTS_DIR, `text${textNumber}.txt`);
        return await fs.readFile(textFile, 'utf-8');
    } catch (error) {
        console.error(`Fehler beim Laden von text${textNumber}.txt:`, error);
        return null;
    }
}

// E-Mail senden
async function sendEmail(to, subject, text) {
    const mailOptions = {
        from: `"Danapfel Digital" <${process.env.SMTP_USER}>`,
        to: to,
        subject: subject,
        text: text,
        html: text.replace(/\n/g, '<br>')
    };

    try {
        const info = await transporter.sendMail(mailOptions);
        console.log(`E-Mail erfolgreich gesendet an ${to}`);
        return true;
    } catch (error) {
        console.error(`Fehler beim Senden an ${to}:`, error.message);
        return false;
    }
}

// Hauptfunktion für das Versenden
async function sendNextEmail() {
    console.log('\n=== Starte E-Mail-Versand ===');

    const state = await loadState();
    const emails = await loadEmails();

    if (emails.length === 0) {
        console.error('Keine E-Mail-Adressen gefunden!');
        return;
    }

    // Nächsten Text bestimmen (1-6 rotierend)
    state.lastTextIndex = (state.lastTextIndex % 6) + 1;
    const textContent = await loadText(state.lastTextIndex);

    if (!textContent) {
        console.error(`Text ${state.lastTextIndex} konnte nicht geladen werden!`);
        return;
    }

    // Nächste E-Mail-Adresse bestimmen
    const emailIndex = state.lastEmailIndex % emails.length;
    const recipientEmail = emails[emailIndex];

    console.log(`Sende Text ${state.lastTextIndex} an: ${recipientEmail}`);

    // E-Mail senden
    const subject = `Danapfel Digital - Ihre digitale Lösung`;
    const success = await sendEmail(recipientEmail, subject, textContent);

    if (success) {
        state.lastEmailIndex = emailIndex + 1;
        await saveState(state);
        console.log('State aktualisiert');
    }

    console.log('=== E-Mail-Versand abgeschlossen ===\n');
}

// Test-Mail senden (für manuelle Tests)
async function sendTestEmail() {
    const testEmail = 'danapfelmichael7@gmail.com';
    const subject = 'Test - Danapfel Digital EmailBot';
    const text = 'Dies ist eine Testmail vom EmailBot. Wenn Sie diese Nachricht erhalten, funktioniert der Bot korrekt!';

    console.log(`Sende Testmail an: ${testEmail}`);
    try {
        await sendEmail(testEmail, subject, text);
        console.log('Testmail erfolgreich versendet!');
    } catch (error) {
        console.error('Testmail Fehler:', error.message);
    }
}

// Cron-Job einrichten (täglich um 10:00 Uhr)
const job = new CronJob(
    '0 10 * * *', // Täglich um 10:00 Uhr
    async () => {
        console.log('Cron-Job gestartet:', new Date().toISOString());
        await sendNextEmail();
    },
    null,
    true,
    'Europe/Berlin'
);

// Server-Status-Endpunkt
const PORT = process.env.BOT_PORT || 3000;

console.log('EmailBot läuft auf Port', PORT);
console.log('Cron-Job aktiv: Täglich um 10:00 Uhr');
console.log('Nächste Ausführung:', job.nextDate().toJSDate().toISOString());

// Test beim Start ausführen (optional)
if (process.argv.includes('--test')) {
    sendTestEmail();
}

// Ermöglicht direkten Aufruf für sofortigen Versand
if (process.argv.includes('--send')) {
    sendNextEmail().then(() => {
        console.log('Einmaliger Versand abgeschlossen');
    });
}
