"""
Sends the weekly Housing Intelligence Digest via email (SMTP/Gmail).
Uses a Gmail App Password — NOT your regular Gmail password.
To set up: Google Account → Security → 2-Step Verification → App Passwords → Create.
"""
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DIGEST_LOG = Path("data/digest_log.json")


def send_digest(html_body, plain_body, recipients=None):
    """
    Send the digest email.
    Reads credentials from environment:
      DIGEST_FROM_EMAIL  — your Gmail address
      DIGEST_APP_PASSWORD — Gmail App Password (not your login password)
      DIGEST_TO_EMAILS   — comma-separated recipient emails
    """
    from_email = os.environ.get("DIGEST_FROM_EMAIL", "")
    app_password = os.environ.get("DIGEST_APP_PASSWORD", "")
    to_emails_str = os.environ.get("DIGEST_TO_EMAILS", "")

    if recipients:
        to_list = recipients
    else:
        to_list = [e.strip() for e in to_emails_str.split(",") if e.strip()]

    if not from_email or not app_password:
        return False, "Missing DIGEST_FROM_EMAIL or DIGEST_APP_PASSWORD in .env"
    if not to_list:
        return False, "No recipients configured"

    subject = f"Housing Intelligence Digest — {date.today().strftime('%d %B %Y')}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Housing Intelligence <{from_email}>"
    msg["To"] = ", ".join(to_list)

    msg.attach(MIMEText(plain_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, app_password)
            server.sendmail(from_email, to_list, msg.as_string())
        return True, f"Sent to {len(to_list)} recipients"
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed — check your Gmail App Password in .env"
    except Exception as e:
        return False, str(e)


def save_digest_html(html_body):
    """Save the latest digest as an HTML file for preview."""
    path = Path("data/latest_digest.html")
    path.write_text(html_body)
    return path
