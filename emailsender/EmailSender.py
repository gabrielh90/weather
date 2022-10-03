"""Email sender helper."""
from email.message import EmailMessage
import logging
import smtplib

from config.ConfigReader import ConfigReader


def SendEmail(receiverEmail, message, port=587, host='smtp.gmail.com') -> bool:
    """Send email.

          Send an email to receiver with message
          Default sender settings are for Gmail accounts.

    Args:
        receiverEmail (_type_): email receiver address
        message (_type_): content of the mail

    Returns:
      bool: True if email was sent, otherwise False
    """
    configData = ConfigReader('emailCredentials').configData

    senderEmail = configData['email']
    password = configData['password']
    port = configData['port']
    host = configData['host']

    email = EmailMessage()
    email['from'] = senderEmail
    email['to'] = receiverEmail
    email['subject'] = 'The weather has changed!'
    email.set_content(message)

    with smtplib.SMTP(host, port) as smtp:
        try:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(senderEmail, password)
            smtp.send_message(email)
            logging.info(f'An email was sent to {receiverEmail}')
        except smtplib.SMTPAuthenticationError:
            logging.error('The username and/or password is incorrect')
            return False
        except Exception as ex:
            logging.error('Unexpected error: ', repr(ex))
            return False

    return True
