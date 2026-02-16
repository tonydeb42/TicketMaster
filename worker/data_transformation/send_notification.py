from worker.worker import app
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

@app.task
def send_notification(message, email):
    try:
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
            <div style="background-color: #fff; border-radius: 8px; padding: 30px; max-width: 600px; margin: 0 auto; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h2 style="color: #388e3c; margin-bottom: 15px;">✅ File Upload Successful</h2>
            <p style="color: #333; font-size: 14px; line-height: 1.6;">{message}</p>
            <p style="color: #666; font-size: 12px; margin-top: 20px;">Thank you for using our service.</p>
            </div>
        </body>
        </html>
        """
        msg = MIMEText(html, "html")
        msg["Subject"] = "File Upload - Success"

        smtp_username = os.getenv("SMTP_USERNAME") or ""
        smtp_password = os.getenv("SMTP_PASSWORD") or ""
        smtp_server = os.getenv("SMTP_SERVER") or ""
        smtp_port = os.getenv("SMTP_PORT") or ""

        if not all([smtp_username, smtp_password, smtp_server, smtp_port]):
            raise ValueError("Missing required SMTP environment variables")

        msg["From"] = smtp_username
        msg["To"] = email

        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        return f"Notification sent to {email} successfully."
    except Exception as e:
        print(f"Error sending notification: {e}")
        raise e
