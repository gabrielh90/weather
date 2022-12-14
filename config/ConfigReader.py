"""Read config files."""
from configparser import ConfigParser
import logging
import sys

from config.Config import Config
from helper.helper import isEmailValid, isFloat


class ConfigReader(Config):
    """Deals with reading config files.

    Args:
        Config : base Config class
    """

    def __init__(self, type='server'):
        """Construct ConfigReader.

        Args:
            type (str, optional): Type of the configuration file.\
            Defaults to 'server'.
        """
        super().__init__(type)
        logging.debug(f'Create Config Reader object{self.type}')
        self.__configData = {}

        self.config = ConfigParser()

        self.readConfigFile()

    def readConfigFile(self):
        """Read the configuration file."""
        try:
            logging.info(f'Reading config file {self.configFilePath}')
            self.config.read(filenames=self.configFilePath)
        except Exception as ex:
            logging.warning(f'Unexpected error: {self.configFilePath} is',
                            repr(ex))
        else:
            logging.debug(self.config)
            if self.type == 'server':
                self.serverConfig()
            elif self.type == 'client':
                self.clientConfig()
            elif self.type == 'emailCredentials':
                self.emailCredentialsConfig()

            logging.info(self.configData)

    def serverConfig(self):
        """Verify and sets server configuration."""
        self.__configData = {
          'town': 'Boston'
        }
        if 'USER' in self.config and self.config['USER']['town']:
            self.__configData['town'] = self.config['USER']['town']
        else:
            logging.critical('Applying default config values for server side!')
            sys.exit()

    def clientConfig(self):
        """Verify and sets client configuration."""
        self.__configData = {
          'email': None,
          'tempThreshold':  0,
          'humidityThreshold':  0,
          'town': '',
          'temp': 0,
          'humidity': 0
        }

        if 'USER' in self.config:
            if 'email' in self.config['USER'] and \
                  isEmailValid(self.config['USER']['email']):
                self.__configData['email'] = self.config['USER']['email']
            else:
                logging.critical('Verify that the email \
is set correct in config file')
                sys.exit()

            if 'tempThreshold' in self.config['USER'] and \
                    isFloat(self.config['USER']['tempThreshold']):
                self.__configData['tempThreshold'] = \
                    float(self.config['USER']['tempThreshold'])
            else:
                logging.critical('Verify temperature threshold \
is set in config file')
                sys.exit()

            if 'humidityThreshold' in self.config['USER'] and \
                    isFloat(self.config['USER']['humidityThreshold']):
                self.__configData['humidityThreshold'] = \
                    float(self.config['USER']['humidityThreshold'])
            else:
                logging.critical('Verify humidity threshold is \
set in config file')
                sys.exit()

            if 'town' in self.config['USER']:
                self.__configData['town'] = self.config['USER']['town']
            if 'temp' in self.config['USER'] and \
                    isFloat(self.config['USER']['temp']):
                self.__configData['temp'] = \
                    self.config.getfloat('USER', 'temp')
            if 'humidity' in self.config['USER'] and \
                    isFloat(self.config['USER']['humidity']):
                self.__configData['humidity'] = \
                    self.config.getfloat('USER', 'humidity')

    def emailCredentialsConfig(self):
        """Verify and sets server configuration."""
        self.__configData = {
          'email': None,
          'password': None,
          'port': 587,
          'host': 'smtp.gmail.com'
        }
        if 'USER' in self.config:
            if 'email' in self.config['USER'] and \
                  isEmailValid(self.config['USER']['email']):
                self.__configData['senderEmail'] = self.config['USER']['email']
            else:
                logging.critical('Verify that the email is set correct \
in config file')
                sys.exit()

            if 'password' in self.config['USER']:
                self.__configData['password'] = self.config['USER']['password']
            else:
                logging.critical('Verify that the password is set \
in config file')
                sys.exit()

            if 'port' in self.config['USER']:
                self.__configData['port'] = self.config['USER']['port']
            if 'host' in self.config['USER']:
                self.__configData['host'] = self.config['USER']['host']

    @property
    def configData(self):
        """Getter for read configuration.

        Returns:
            dictionary: configuration dat
        """
        return self.__configData
