import 'dotenv/config';
import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT || '587'),
    secure: false,
    auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS
    },
    tls: {
        rejectUnauthorized: false
    },
    debug: true,
    logger: true
});

// Verify connection
console.log('Testing SMTP connection...');
console.log('Host:', process.env.SMTP_HOST);
console.log('Port:', process.env.SMTP_PORT);
console.log('User:', process.env.SMTP_USER);
console.log('');

transporter.verify(function (error, success) {
    if (error) {
        console.log('❌ SMTP Connection Error:');
        console.log(error);
    } else {
        console.log('✅ Server is ready to take our messages');

        // Send test email
        const mailOptions = {
            from: `"Danapfel Digital Test" <${process.env.SMTP_USER}>`,
            to: 'danapfelmichael7@gmail.com',
            subject: 'Test Email - ' + new Date().toISOString(),
            text: 'Dies ist eine Testmail mit vollem Debugging. Zeitstempel: ' + new Date().toLocaleString('de-DE'),
            html: '<p>Dies ist eine <strong>Testmail</strong> mit vollem Debugging.</p><p>Zeitstempel: ' + new Date().toLocaleString('de-DE') + '</p>'
        };

        console.log('\nSending test email...');
        transporter.sendMail(mailOptions, (error, info) => {
            if (error) {
                console.log('❌ Send Error:', error);
            } else {
                console.log('✅ Email sent successfully!');
                console.log('Message ID:', info.messageId);
                console.log('Response:', info.response);
                console.log('Accepted:', info.accepted);
                console.log('Rejected:', info.rejected);
                console.log('Full info:', JSON.stringify(info, null, 2));
            }
        });
    }
});
