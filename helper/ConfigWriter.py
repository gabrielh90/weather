from configparser import ConfigParser
import logging

from .Config import Config

class ConfigWriter(Config):
  """Deals with writing config files

  Args:
      Config : base Config class
  """
  def __init__(self, type = 'server'):
    """Constructor for ConfigWriter

    Args:
        type (str, optional): Type of the configuration file. Defaults to 'server'.
    """
    super().__init__(type)
    self.config = ConfigParser()

  def serverConfig(self, town = ''):
    """Server configuration

    Args:
        town (str, optional): Town to be queried for weather . Defaults to ''.
    """
    self.config.remove_section('USER')
    self.config['USER'] = {
      'town': town
    }

  def clientConfig(self, email, tempThreshold, humidityThreshold, town, temp, humidity):
    """Client configuration

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
      'tempthreshold': tempThreshold,
      'humiditythreshold': humidityThreshold,
      'town': town,
      'temp': temp,
      'humidity': humidity
    }

  def writeConfigFile(self):
    """Writes configuration to file
    """
    logging.info(f'Config file path: {self.filepathConfig}')
    try:
      with open(self.filepathConfig, 'w') as f:
        self.config.write(f)
    except Exception as ex:
      logging.error(f'Unexpected error: {self.filepathConfig} is', repr(ex))


if __name__ == '__main__':
  log_dir = '/var/log/weatherhelper.log'
  logging.basicConfig(filename=log_dir, 
                      level=logging.DEBUG,
                      filemode='a',
                      format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

  cw = ConfigWriter()
  cw.serverConfig('Burundi')
  cw.writeConfigFile()
  
  cw.type = 'client'
  cw.clientConfig('johndoe@gmail.com', 1, 2, 3, 4, 5)
  cw.writeConfigFile()  
