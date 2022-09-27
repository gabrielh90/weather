from configparser import ConfigParser
import logging
import re

from helper.Config import Config

class ConfigReader(Config):
  """Deals with reading config files

  Args:
      Config : base Config class
  """
  pattern = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"

  def __init__(self, type = 'server'):
    """Constructor for ConfigReader

    Args:
        type (str, optional): Type of the configuration file. Defaults to 'server'.
    """
    super().__init__(type)
    self.__configData = {}
    
    self.config = ConfigParser()

    self.readConfigFile()

  def readConfigFile(self):
    """Reads the configuration file
    """
    try:
      logging.info(f'Reading config file {self.filepathConfig}')
      self.config.read(filenames = self.filepathConfig)
    except Exception as ex:
      logging.warning(f'Unexpected error: {self.filepathConfig} is', repr(ex))
    # else:
    #   logging.info(self.config)
    finally:
      if self.type == 'server':
        self.serverConfig()
      else:
        self.clientConfig()

  def serverConfig(self):
    """Verify and sets server configuration
    """
    self.__configData = {
      'town': 'Botosani'
    }
    if 'USER' in self.config and self.config['USER']['town']:
      self.__configData['town'] = self.config['USER']['town']
    else:
      logging.warning('Applying default config values for server side!')

    logging.info(self.configData)

  def clientConfig(self):
    """Verify and sets client configuration
    """
    self.__configData = {
      'email': None,
      'tempthreshold':  0,
      'humiditythreshold':  0,
      'town': '',
      'temp' : 0,
      'humidity': 0
    }

    if 'USER' in self.config:
      if 'email' in self.config['USER'] and self.__isEmailValid(self.config['USER']['email']):
          self.__configData['email'] = self.config['USER']['email']
      else:
        logging.exception('Verify that the email is set in config file')
        # raise Exception('Verify that the email is correct')

      if 'tempthreshold' in self.config['USER'] and self.isFloat(self.config['USER']['tempthreshold']):
        self.__configData['tempthreshold'] = float(self.config['USER']['tempthreshold'])
      else:
        logging.warning('Verify temperature threshold is set in config file')

      if 'humiditythreshold' in self.config['USER'] and self.isFloat(self.config['USER']['humiditythreshold']):
        self.__configData['humiditythreshold'] = float(self.config ['USER']['humiditythreshold'])
      else:
        logging.warning('Verify humidity threshold is set in config file')

      if 'town' in self.config['USER']:
          self.__configData['town'] = self.config['USER']['town']
      if 'temp' in self.config['USER'] and self.isFloat(self.config['USER']['temp']):
        self.__configData['temp'] = self.config.getfloat('USER', 'temp')
      if 'humidity' in self.config['USER'] and self.isFloat(self.config['USER']['humidity']):
        self.__configData['humidity'] = self.config.getfloat('USER', 'humidity')

    logging.info(self.configData)

  @property
  def configData(self):
    """ Getter for read configuration

    Returns:
        dictionary: configuration dat
    """
    return self.__configData

  def __isEmailValid(self, email) -> bool:
    """Validate email

    Args:
        email (string): email to be verified

    Returns:
        bool: True - email is valid, otherwise False
    """
    if re.match(self.pattern, email):
      return True
    else:
      return False
  
  def isFloat(self, value):
    """Check if the given value is float

    Args:
        value (string): value to be tested

    Returns:
        bool: True - value is float, otherwise False
    """
    try:
      float(value)
      return True
    except ValueError:
      return False



if __name__ == '__main__':
  log_dir = '/var/log/weatherhelper.log'
  logging.basicConfig(filename=log_dir, 
                      level=logging.DEBUG,
                      filemode='a',
                      format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

  cr = ConfigReader()
  town = cr.configData['town']

  cr.type = 'client'
  cr.readConfigFile()
  emailReceiver = cr.configData['email']
  tempthreshold = cr.configData['tempthreshold']
  