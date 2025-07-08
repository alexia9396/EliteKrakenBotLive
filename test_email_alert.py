import smtplib
from email.mime.text import MIMEText

# === Fill in your details below ===
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "alexia.delaney9396@gmail.com"           # 🔁 Replace with your Gmail address
EMAIL_PASSWORD = "zckl vbnx pdsc cmhs"  # 🔁 Use Gmail App Password (not normal password)
TO_EMAIL = "alexia.delaney9396@gmail.com"                # 🔁 Or your phone's email-to-text gateway

# === Email content ===
subject = "✅ Test Alert from EliteKrakenBotLive"
body = "This is a test email to confirm alert delivery is working."

# Create MIMEText object
msg = MIMEText(body)
msg["From"] = EMAIL_ADDRESS
msg["To"] = TO_EMAIL
msg["Subject"] = subject

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
    server.quit()
    print("✅ Test email sent successfully!")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
