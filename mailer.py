import os
import secrets
import string
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load local .env file if running locally
load_dotenv()

def generate_temporary_password(length: int = 15) -> str:
    """Generates a cryptographically strong random password."""
    pool = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(pool) for _ in range(length))

def build_email_message(sender: str, recipient: str, temp_password: str) -> EmailMessage:
    """Constructs the MIME email message."""
    msg = EmailMessage()
    msg["Subject"] = "Your One-Time Temporary Password"
    msg["From"] = sender
    msg["To"] = recipient
    msg.set_content(
        f"Hello,\n\n"
        f"Your temporary password is: {temp_password}\n\n"
        f"Please log in and update it immediately.\n\n"
        f"IT Support"
    )
    return msg

def send_email(msg: EmailMessage) -> bool:
    """Connects to SMTP, upgrades to TLS, and dispatches the email."""
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    if not sender_email or not sender_password:
        raise ValueError("Missing EMAIL_USER or EMAIL_PASS environment variables.")

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, sender_password)
        server.send_message(msg)
    return True

def main():
    recipient = os.getenv("TARGET_RECIPIENT", "recipient@example.com")
    sender = os.getenv("EMAIL_USER")
    
    password = generate_temporary_password(15)
    message = build_email_message(sender, recipient, password)
    
    try:
        send_email(message)
        print(f"[+] Password successfully delivered to {recipient}")
    except Exception as err:
        print(f"[!] Delivery failed: {err}")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
