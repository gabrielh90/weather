"""Email sender helper."""
from config import ConfigReader
from email.message import EmailMessage
from helper.helper import isEmailValid
import logging
import smtplib
# sys.path.append('./../')


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

    if not isEmailValid(senderEmail) or not isEmailValid(receiverEmail):
        logging.error('Verify that the email is set correct in config file\
 (eg: johndoe@gmail.com)')
        # raise Exception('Verify that the email is correct')
        # sys.exit()
        return False

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
