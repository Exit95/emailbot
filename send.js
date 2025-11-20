import 'dotenv/config';
import nodemailer from 'nodemailer';
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
        rejectUnauthorized: false
    }
});

// State laden
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

// Text laden
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
        console.log(`✓ E-Mail erfolgreich gesendet an ${to}`);
        return true;
    } catch (error) {
        console.error(`✗ Fehler beim Senden an ${to}:`, error.message);
        return false;
    }
}

// Hauptfunktion
async function main() {
    console.log('\n╔════════════════════════════════════════╗');
    console.log('║   Danapfel Digital - E-Mail Versand   ║');
    console.log('╚════════════════════════════════════════╝\n');

    const state = await loadState();
    const emails = await loadEmails();

    if (emails.length === 0) {
        console.error('❌ Keine E-Mail-Adressen gefunden!');
        process.exit(1);
    }

    // Nächsten Text bestimmen
    state.lastTextIndex = (state.lastTextIndex % 6) + 1;
    const textContent = await loadText(state.lastTextIndex);

    if (!textContent) {
        console.error(`❌ Text ${state.lastTextIndex} konnte nicht geladen werden!`);
        process.exit(1);
    }

    // Nächste E-Mail-Adresse
    const emailIndex = state.lastEmailIndex % emails.length;
    const recipientEmail = emails[emailIndex];

    console.log(`📧 Empfänger: ${recipientEmail}`);
    console.log(`📄 Text: ${state.lastTextIndex}/6`);
    console.log(`📊 Fortschritt: ${emailIndex + 1}/${emails.length}\n`);

    // E-Mail versenden
    const subject = 'Danapfel Digital - Ihre digitale Lösung';
    const success = await sendEmail(recipientEmail, subject, textContent);

    if (success) {
        state.lastEmailIndex = emailIndex + 1;
        await saveState(state);
        console.log('\n✓ State aktualisiert');
        console.log('═══════════════════════════════════════\n');
        process.exit(0);
    } else {
        console.log('\n✗ E-Mail konnte nicht gesendet werden');
        console.log('═══════════════════════════════════════\n');
        process.exit(1);
    }
}

// Ausführen
main().catch(error => {
    console.error('Kritischer Fehler:', error);
    process.exit(1);
});
