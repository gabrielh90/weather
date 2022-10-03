"""Configure logging system."""
import logging
import logging.handlers as handlers
import os
from helper.helper import getCommandLineArgument


class ConfigLogs():
    """Config logging class."""

    def __init__(self, filename='weather.log', level='debug') -> None:
        """Initialize script logging.

          WARNING: There should be no 'logging' print before basicConfig call
        Args:
            filename (str, optional): Absolute filepath to log destination or
                                      relative to current running directory.
                                      Defaults to 'weather.log'.
            level (str, optional): Logging verbosity level.
                                  Defaults to 'debug'.
        """
        self.filename = os.path.expanduser('~') + filename
        self.level = None
        self.formatter = '%(asctime)s %(levelname)s %(filename)s\
 : %(funcName)s (%(lineno)d) %(message)s'

        argFilename = getCommandLineArgument('d', 'dump' + 'FileName')
        if argFilename:
            self.filename = argFilename

        verbosityLevel = getCommandLineArgument('v', 'verbosityLevel')
        if verbosityLevel:
            self.strToEnumVerbosityLevel(verbosityLevel)
            if not self.level:
                logging.error(f'Incorrect command line value for\
verbosity level! Given: \'{verbosityLevel}\', supported: debug, info, warning')

        if not self.level:
            self.strToEnumVerbosityLevel(level)
            if not self.level:
                logging.warning(f'Incorrect argument value for verbosity\
 level! Given: \'{level}\', supported: debug, info, warning')
                self.level = logging.WARNING

        logging.basicConfig(filename=self.filename,
                            filemode='a',
                            format=self.formatter,
                            level=self.level)

    def strToEnumVerbosityLevel(self, level):
        """Convert string verbosity level to enum.

        Args:
            level (str): verbosity level
        """
        if str(level) == 'debug':
            self.level = logging.DEBUG
        elif str(level) == 'info':
            self.level = logging.INFO
        elif str(level) == 'warning':
            self.level = logging.WARNING

    def setupRotatingLogs(self, filename=None, level=None, maxBytes=5):
        """Keep in check file logging size.

        Args:
            filename (_type_, optional): _description_. Defaults to None.
            level (_type_, optional): _description_. Defaults to None.
            maxBytes (int, optional): _description_. Defaults to 5.
        """
        if filename:
            self.filename = filename
        if level:
            self.strToEnumVerbosityLevel(level)

        my_handler = handlers.RotatingFileHandler(self.filename, mode='a',
                                                  maxBytes=maxBytes,
                                                  backupCount=0)
        my_handler.setLevel(self.level)
        my_handler.setFormatter(logging.Formatter(self.formatter))
        logging.getLogger().addHandler(my_handler)
