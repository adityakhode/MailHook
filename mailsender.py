import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException

def send_notification_to_admin(username: str, email: str, query: str):
    # Admin email address
    admin_email = "admin_email"

    # Sender email credentials
    sender_email = "your email"
    sender_password = "your password"

    # Email subject and body
    subject = "New Query Submitted"
    body = f"""
    A new query has been submitted:

    Username: {username}
    Email: {email}
    Query: {query}

    Please check the system for more details.
    """

    try:
        # Set up the MIME structure
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = admin_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email notification.")



