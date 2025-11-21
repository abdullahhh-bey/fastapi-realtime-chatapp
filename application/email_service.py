import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "abdullahamirr9@example.com"
SMTP_PASSWORD = "rplj avny qhyk tnqs"

def send_email(to_email: str, subject: str, html_content: str):

    message = MIMEMultipart()
    message["From"] = SMTP_EMAIL
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, to_email, message.as_string())
