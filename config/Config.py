"""Base config file."""
import logging
import os
import sys

from helper.helper import getCommandLineArgument


class Config():
    """Base class for Config."""

    def __init__(self, type='server'):
        """Construct Config Object.

        Args:
            type (str, optional): Type of the configuration file.
            Defaults to 'server'.
        """
        self.type = type

    @property
    def type(self):
        """Getter for configuration file type.

        Returns:
            str: Type of the configuration file
        """
        return self.__type

    @type.setter
    def type(self, value):
        """Setter for configuration file type\
 supported values: client or 'server'.

        Args:
            value (str): Type of the configuration file
        """
        if value in ('client', 'server', 'emailCredentials'):
            self.__type = value
            filename = getCommandLineArgument(value[0], value + 'FileName')
            if filename:
                self.setConfigFilePath(filename)
            else:
                self.setConfigFilePath()
        else:
            logging.error('The type must be \'server\', \
\'client\', or \'credential\'')
            sys.exit(1)

    def setConfigFilePath(self, filePath=None):
        """Set the filepath of configuration\
 file base on the supported types."""
        if filePath:
            if os.path.isfile(filePath):
                self.configFilePath = filePath
            else:
                logging.error(f'Configuration {self.type} file \
does not exist: {filePath}')
                sys.exit(1)
        else:
            self.configFilePath = os.path.expanduser('~')
            self.configFilePath += '/WeatherConfig' + self.type.title()
            self.configFilePath += '.ini'
            if not os.path.isfile(self.configFilePath):
                logging.error(f'Configuration {self.type} file \
does not exist: {self.configFilePath}')
                sys.exit(1)
