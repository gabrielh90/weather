"""Weather data file communication."""
import logging
import json

from helper.helper import isFloat


def setWeatherData(weatherForecast):
    """Write to file weather for inter applications communication.

    Args:
        weatherForecast (dictionary): town, temperature and humidity
    """
    try:
        fileName = '/tmp/WeatherData.txt'
        logging.info(f'Writing weather data file {fileName}')
        with open(fileName, 'w') as f_obj:
            json.dump(weatherForecast, f_obj)
    except Exception as ex:
        logging.error(f'Unexpected error: {fileName} is', repr(ex))
        exit()


def getWeatherData():
    """Read from file weather for inter applications communication.

    Returns:
        list: town, temperature and humidity
    """
    currTown = currTemp = currHumidity = None

    try:
        fileName = '/tmp/WeatherData.txt'
        logging.info(f'Reading weather data file {fileName}')
        with open(fileName, 'r+') as f_obj:
            weatherForecast = json.load(f_obj)
    except FileNotFoundError:
        logging.exception('Can’t find {0}.'.format(fileName))
        exit()
    except Exception as ex:
        logging.error(f'Unexpected error: {fileName} is', repr(ex))
        exit()
    else:
        logging.info(weatherForecast)

        if 'town' in weatherForecast:
            currTown = weatherForecast['town']

        if 'temp' in weatherForecast and isFloat(weatherForecast['temp']):
            currTemp = float(weatherForecast['temp'])

        if 'humidity' in weatherForecast and \
                isFloat(weatherForecast['humidity']):
            currHumidity = float(weatherForecast['humidity'])

        return [currTown, currTemp, currHumidity]
