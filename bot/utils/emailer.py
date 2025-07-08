import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bot.utils.logger import setup_logger

logger = setup_logger("Emailer")

class Emailer:
    def __init__(self, sender_email, sender_password, recipient_email):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465

    def send_email(self, subject, body):
        try:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.recipient_email
            message["Subject"] = subject

            message.attach(MIMEText(body, "plain"))
            text = message.as_string()

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.recipient_email, text)

            logger.info(f"📧 Email sent: {subject}")
        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")
