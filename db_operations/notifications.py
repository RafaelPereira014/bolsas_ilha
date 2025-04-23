

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib

import pymysql
from config import db_config  # Import the database configuration


def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return pymysql.connect(**db_config)


def send_email(to_emails, subject, message, attachments=[]):
    try:
        # SMTP server configuration
        smtp_server = 'pegasus.azores.gov.pt'
        smtp_port = 587
        user = 's0204bolsasilhaapp'
        password = 'oUrR9xhPtEmFi9Cs'
        from_email = 'noreply@azores.gov.pt'

        # Create a secure SSL context
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(user, password)
            print(f"Sending email to: {to_emails}")  # Add this to debug the recipient email

            for to_email in to_emails:
                # Create a MIMEMultipart object to represent the email
                print(f"Sending email to: {to_email}")  # Add this to debug the recipient email

                msg = MIMEMultipart()
                msg['From'] = from_email
                msg['To'] = to_email
                msg['Subject'] = subject

                # Attach the message body
                msg.attach(MIMEText(message, 'html'))

                # Attach files if provided
                for attachment_path in attachments:
                    try:
                        filename = os.path.basename(attachment_path)  # Extract filename from path
                        # Open the file in binary mode
                        with open(attachment_path, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename="{filename}"',  # Correctly set the filename here
                            )
                            msg.attach(part)
                    except Exception as e:
                        print(f"Failed to attach file {attachment_path}: {e}")

                # Send the email
                server.sendmail(from_email, to_email, msg.as_string())

        print("Emails sent successfully")

    except Exception as e:
        print(f"Failed to send email: {e}")
        
def send_email_on_selection(sgc, recipient_emails, mensagem):
    subject = f"Proposta de colocação com base no SGC - {sgc}."
    message = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .email-container {{ padding: 20px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9; }}
            .header {{ font-size: 18px; font-weight: bold; color: #333; }}
            .content {{ margin-top: 10px; }}
            .footer {{ margin-top: 20px; font-size: 12px; color: #666; }}
            .table {{width: 100%;border-collapse: collapse;margin-top: 20px;}}
            .th, td {{
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }}

            .th {{
                background-color: #f2f2f2;
                color: #333;
                font-weight: bold;
            }}

            .tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}

            .tr:hover {{
                background-color: #e9e9e9;
            }}

            .table-container {{
                overflow-x: auto;
                margin-top: 20px;
            }}
        </style>
    
    </head>
    <body>
        <div class="email-container">
           
            <div class="content">
                <p>{mensagem}</p>
            </div>
            <div class="footer">
                <p>Obrigado,<br>A Equipa GBI</p>
            </div>
        </div>
    </body>
    </html>
    """
    # Call the function to send the email
    send_email(recipient_emails, subject, message)

    # Return a tuple with a status message and a status code
    return {"status": "success", "message": "Email sent successfully"}, 200