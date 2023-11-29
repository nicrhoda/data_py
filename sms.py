import email, smtplib, ssl
from providers import PROVIDERS
import os
from decouple import config

# sends sms message using email address and project specific password
def send_sms_via_email(number:str, message:str, provider:str, sender_credentials:tuple, subject:str="message sent using python", smtp_server="smtp.gmail.com", smtp_port: int = 465):
    sender_email, email_password = sender_credentials
    reciever_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'

    # sending message with input params
    email_message = f"Subject:{subject}\nTo:{reciever_email}\n{message}"

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ssl.create_default_context()) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, reciever_email, email_message)

# assembles message with params and message and sends it
def main(inputmessage):
    print("sending message...")
    number = config('phone_number')
    message = inputmessage
    provider = config('provider')
    sender_credentials = (config('email'), config('password'))
    send_sms_via_email(number, message, provider, sender_credentials)
    print("message sent")

