from worker.worker import app
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

@app.task(bind=True)
def failure_notification(self, task_id, email=None):
    try:
        result = self.app.AsyncResult(task_id)
        exc = result.result
        traceback = result.traceback

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.0
        )

        prompt = f"""
        Summarize this error in 2-3 lines max.
        Focus on root cause only.

        Error:
        {exc}

        Traceback:
        {traceback}
        """

        summary = llm.invoke(prompt).content.strip()

        message = f"""
Task failed: {task_id}

Summary:
{summary}

Full Error:
{exc}
"""

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background:#f5f5f5; padding:20px;">
            <div style="background:#fff; border-radius:8px; padding:30px; max-width:600px; margin:auto;">
                <h2>File Upload Failed</h2>
                <pre>{message}</pre>
            </div>
        </body>
        </html>
        """

        msg = MIMEText(html, "html")
        msg["Subject"] = "File Upload - Error"

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
