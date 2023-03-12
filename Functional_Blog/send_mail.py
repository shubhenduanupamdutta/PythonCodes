import smtplib
from email.message import EmailMessage

MAIL_ID = "YOUR_MAIL_ID"
PASSWORD = "YOUR_PASSWORD"

# tHIS code is for when you have outlook mail id. i.e. office365 mail ID>

# Trying with message object
def send_me_mail(email_message: str):
    with smtplib.SMTP("smtp.office365.com", port=587) as connection:
            connection.starttls()
            connection.login(MAIL_ID, PASSWORD)
            message = EmailMessage()
            message.set_content(email_message)
            message['Subject'] = f"You have a new mail from your blog."
            message["To"] = "TO_MAIL_ID"
            message["From"] = MAIL_ID
            connection.send_message(message)

