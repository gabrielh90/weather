"""Write configuration to file."""
from configparser import ConfigParser
import logging
from .Config import Config


class ConfigWriter(Config):
    """Deals with writing config files.

    Args:
        Config : base Config class
    """

    def __init__(self, type='server'):
        """Construct for ConfigWriter.

        Args:
            type (str, optional): Type of the configuration file.
                                  Defaults to 'server'.
        """
        super().__init__(type)
        logging.debug('Create Config Writer object')
        self.config = ConfigParser()

    def serverConfig(self, town=''):
        """Server configuration.

        Args:
            town (str, optional): Town to be queried for weather .
                                  Defaults to 'Boston'.
        """
        self.config.remove_section('USER')
        self.config['USER'] = {
          'town': town
        }

    def clientConfig(self, email, tempThreshold, humidityThreshold,
                     town, temp, humidity):
        """Client configuration.

        Args:
            email (str): Client receiver email
            tempThreshold (str): Temperature threshold
            humidityThreshold (str): Humidity threshold
            town (str): Queried town for weather
            temp (str): Received temperature for town filed
            humidity (str): Received humidity for town filed
        """
        self.config.remove_section('USER')
        self.config['USER'] = {
          'email': email,
          'tempThreshold': tempThreshold,
          'humidityThreshold': humidityThreshold,
          'town': town,
          'temp': temp,
          'humidity': humidity
        }

    def writeConfigFile(self):
        """Write configuration to file."""
        logging.info(f'Config file path: {self.configFilePath}')
        try:
            with open(self.configFilePath, 'w') as f:
                self.config.write(f)
        except Exception as ex:
            logging.error(f'Unexpected error: {self.configFilePath} is',
                          repr(ex))
