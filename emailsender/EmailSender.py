import smtplib
from email.message import EmailMessage
import logging

def SendEmail(emailReceiver, message):
  """Sends an email to a Gmail client

  Args:
      emailReceiver (string): email address
      message (string): content of the mail
  """
  
  port = 587
  host = 'smtp.gmail.com'
  emailSender = ''
  password = ''

  email = EmailMessage()
  email['from'] = emailSender
  email['to'] = emailReceiver
  email['subject'] = 'The weather has changed!'
  email.set_content(message)
  
  with smtplib.SMTP(host, port) as smtp:
    try:
      smtp.ehlo()
      smtp.starttls()
      smtp.login(emailSender, password)
      smtp.send_message(email)
      logging.info(f'An email was sent to {emailReceiver}')
    except smtplib.SMTPAuthenticationError:
      logging.error('The username and/or password is incorrect')
    except Exception as ex:
      logging.error(f'Unexpected error:', repr(ex))
    finally:
      smtp.quit()
