import logging
import os

class Config():
  """Base class for Config
  """
  def __init__(self, type = 'server'):
    """Constructor for Config

    Args:
        type (str, optional): Type of the configuration file. Defaults to 'server'.
    """
    self.type = type

  @property
  def type(self):
    """Getter for configuration file type 

    Returns:
        str: Type of the configuration file
    """
    return self.__type

  @type.setter
  def type(self, value):
    """Setter for configuration file type 
        Supported values: client or 'server'

    Args:
        value (str): Type of the configuration file
    """
    if value in ('client', 'server'):
      self.__type = value
      self.setConfigFilePath()
    else:
      self.__type = 'server'
      logging.warning('The type must be \'server\' or \'client\'')

  def setConfigFilePath(self):
    """Sets the filepath of configuration file base on the supported types
    """
    self.filepathConfig = os.path.expanduser('~')
    if self.type == 'server':
      self.filepathConfig += '/weatherconfigserver.ini'
    else:
      self.filepathConfig += '/weatherconfigclient.ini'
