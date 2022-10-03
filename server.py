"""Server endpoint."""
import logging
from helper.API import API
from config.ConfigReader import ConfigReader
from config.ConfigLogs import ConfigLogs
from helper.WeatherSharedMemoryCommunication import setWeatherData
from helper.helper import getCommandLineArgument


def server():
    """Get weather from an API and logs the gathered data into a file.

    1. Configure logging system
    2. Read configuration file
    3. Make API request
    4. Write gathered data to file
    """
    help = getCommandLineArgument('h', 'help')
    print(help)
    ConfigLogs()

    configRead = ConfigReader('server')
    town = configRead.configData['town']
    logging.info(town)

    api = API(town)
    if api.weatherForecast['temp'] is None or \
       api.weatherForecast['humidity'] is None:
        logging.error('Could not collect the temperature and humidity!')
        exit()
    else:
        logging.info(api.weatherForecast)

    setWeatherData(api.weatherForecast)


if __name__ == '__main__':
    server()
