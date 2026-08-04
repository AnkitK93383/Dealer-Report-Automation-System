import os
import smtplib
from email.message import EmailMessage


def send_email(
    sender_email,
    app_password,
    receiver_email,
    subject,
    body,
    attachment_path
):
    """
    Send an email with an attachment.

    Returns:
        True if the email is sent successfully.

    Raises:
        Exception if sending fails.
    """

    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content(body)

    with open(attachment_path, "rb") as file:
        file_data = file.read()

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="octet-stream",
        filename=os.path.basename(attachment_path)
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(
            sender_email,
            app_password
        )

        smtp.send_message(msg)

    return True