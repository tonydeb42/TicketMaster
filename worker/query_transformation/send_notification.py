from worker.worker import app
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import json
import uuid

load_dotenv()

@app.task
def send_notification(employee_json, email):
    try:
        employee = employee_json
        ticket_id = str(uuid.uuid4())

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background:#f5f7fa; padding:20px;">
            <div style="max-width:650px;margin:auto;background:#ffffff;
                        padding:30px;border-radius:10px;
                        box-shadow:0 2px 6px rgba(0,0,0,0.08);">

                <h2 style="color:#2e7d32;margin-bottom:10px;">
                    ✅ Ticket Successfully Assigned
                </h2>

                <p style="font-size:14px;color:#333;">
                    Your ticket has been reviewed and assigned to the most
                    suitable employee.
                </p>

                <div style="background:#f1f3f6;padding:15px;
                            border-radius:6px;margin:20px 0;">
                    <strong>Ticket ID:</strong> {ticket_id}
                </div>

                <h3 style="margin-bottom:8px;color:#444;">
                    Assigned Employee Details
                </h3>

                <ul style="font-size:14px;color:#333;line-height:1.6;">
                    <li><strong>Name:</strong> {employee.get("Name")}</li>
                    <li><strong>Role:</strong> {employee.get("Role/title")}</li>
                    <li><strong>Department:</strong> {employee.get("Department")}</li>
                    <li><strong>Email:</strong> {employee.get("Email")}</li>
                    <li><strong>Primary Skills:</strong> {employee.get("Primary skills")}</li>
                    <li><strong>Secondary Skills:</strong> {employee.get("Secondary skills")}</li>
                    <li><strong>Experience:</strong> {employee.get("Experience years")} years</li>
                    <li><strong>Domains:</strong> {employee.get("Problem domains handled")}</li>
                </ul>

                <p style="font-size:13px;color:#555;margin-top:20px;">
                    The assigned engineer should contact you shortly.
                    If you need urgent assistance or believe this assignment
                    is incorrect, please reply to this email.
                </p>

                <hr style="margin:25px 0;border:none;border-top:1px solid #eee;">

                <p style="font-size:12px;color:#888;">
                    Automated ticket assignment system • Do not reply unless necessary.
                </p>
            </div>
        </body>
        </html>
        """

        msg = MIMEText(html, "html")
        msg["Subject"] = f"Ticket Assigned | ID: {ticket_id}"

        smtp_username = os.getenv("SMTP_USERNAME") or ""
        smtp_password = os.getenv("SMTP_PASSWORD") or ""
        smtp_server = os.getenv("SMTP_SERVER") or ""
        smtp_port = os.getenv("SMTP_PORT") or ""

        if not all([smtp_username, smtp_password, smtp_server, smtp_port]):
            raise ValueError("Missing SMTP environment variables")

        msg["From"] = smtp_username
        msg["To"] = email

        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        return f"Ticket assignment notification sent to {email}"

    except Exception as e:
        print(f"Error sending assignment email: {e}")
        raise e
