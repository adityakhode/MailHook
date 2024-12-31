import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from Src.loadCredentials import getCredentials

#load credentials
ADMIN_EMAIL, ADMIN_PASSWORD, MANAGER_EMAIL = getCredentials()

def send_notification_to_admin(username: str, email: str, query: str, MANAGER_EMAIL= MANAGER_EMAIL, ADMIN_EMAIL =ADMIN_EMAIL, ADMIN_PASSWORD=ADMIN_PASSWORD):
    
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
        message["From"] = ADMIN_EMAIL
        message["To"] = MANAGER_EMAIL
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(ADMIN_EMAIL, ADMIN_PASSWORD)
            server.send_message(message)

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email notification.")
