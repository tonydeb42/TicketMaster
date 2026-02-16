from worker.worker import app
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

@app.task(bind=True)
def failure_notification(self, task_id, email=None):
    try:
        result = self.app.AsyncResult(task_id)
        exc = result.result
        traceback = result.traceback

        message = f"""
Task failed: {task_id}

Error:
{exc}

Traceback:
{traceback}
"""

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background:#f5f5f5; padding:20px;">
            <div style="background:#fff; border-radius:8px; padding:30px; max-width:600px; margin:auto;">
                <h2>Ticket Assignment Failed</h2>
                <pre>{message}</pre>
            </div>
        </body>
        </html>
        """

        msg = MIMEText(html, "html")
        msg["Subject"] = "Ticket Assignment - Error"

        smtp_username = os.getenv("SMTP_USERNAME") or ""
        smtp_password = os.getenv("SMTP_PASSWORD") or ""
        smtp_server = os.getenv("SMTP_SERVER") or ""
        smtp_port = os.getenv("SMTP_PORT") or ""

        if not all([smtp_username, smtp_password, smtp_server, smtp_port]):
            raise ValueError("Missing SMTP config")

        msg["From"] = smtp_username
        msg["To"] = email or smtp_username

        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        return f"Failure notification sent to {email}"

    except Exception as e:
        raise e
