"""Email sender helper."""
import getopt
import os
import sys
import logging
import smtplib
from email.message import EmailMessage
from configparser import ConfigParser
# sys.path.append('./../')
from helper.helper import isEmailValid


def SendEmail(receiverEmail, message, port=587, host='smtp.gmail.com'):
    """Send email.

          Send an email to receiver with message
          Default sender settings are for Gmail accounts.

    Args:
        receiverEmail (_type_): email receiver address
        message (_type_): content of the mail
        port (int, optional): server email port. Defaults to 587.
        host (str, optional): server email host. Defaults to 'smtp.gmail.com'.
    """
    filePathConfig = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:', ['credentialFilename='])
    except getopt.GetoptError as err:
        logging.error(err)
    else:
        for opt, arg in opts:
            if opt in ('-c', '--credentialFileName'):
                filePathConfig = arg

    if not os.path.isfile(filePathConfig):
        filePathConfig = os.path.expanduser('~') + '/.secret.conf'
        if not os.path.isfile(filePathConfig):
            logging.error(f'Sender email credentials file \
does not exist: {filePathConfig}')
            # raise Exception('Verify that the email is correct')
            sys.exit()
            return False

    config = ConfigParser()
    try:
        logging.debug(
            f'Reading sender email credentials from file {filePathConfig}')
        config.read(filenames=filePathConfig)
    except Exception as ex:
        logging.warning(f'Unexpected error: {filePathConfig} is', repr(ex))
    else:
        if 'USER' in config:
            if 'email' in config['USER'] and \
                  isEmailValid(config['USER']['email']):
                senderEmail = config['USER']['email']
            else:
                logging.error('Verify that the email is set in config file')
                # raise Exception('Verify that the email is correct')
                # sys.exit()
                return False

            if 'password' in config['USER']:
                password = config['USER']['password']
            else:
                logging.error('Verify that the password is set in config file')
                # raise Exception('Verify that the email is correct')
                # sys.exit()
                return False

    if not isEmailValid(receiverEmail):
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


if __name__ == '__main__':
    logging.basicConfig(filename='weather.log',
                        level=logging.DEBUG,
                        filemode='a',
                        format='%(asctime)s - %(levelname)s \
                        - %(name)s - %(message)s')

    SendEmail('dummy', 'dummy')
    SendEmail('johndoe@gmail.com', 'pass')
