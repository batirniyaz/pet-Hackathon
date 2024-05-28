from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from fastapi import BackgroundTasks

SENDGRID_API_KEY = 'your_sendgrid_api_key_here'
FROM_EMAIL = 'your_email@example.com'  # This should be the email you verified with SendGrid

def send_email(email_to: str, subject: str, body: str):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=email_to,
        subject=subject,
        html_content=body)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

async def send_verification_email(background_tasks: BackgroundTasks, email_to: str, verification_code: str):
    subject = "Verify Your Email"
    body = f"<strong>Your verification code is {verification_code}</strong>"
    background_tasks.add_task(send_email, email_to, subject, body)
