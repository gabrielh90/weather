"""Send client weather update emails."""
import logging
from emailsender.EmailSender import SendEmail
from config.ConfigLogs import ConfigLogs
from config.ConfigReader import ConfigReader
from config.ConfigWriter import ConfigWriter
from helper.WeatherSharedMemoryCommunication import getWeatherData
from helper.helper import getCommandLineArgument, getHelper


def client():
    """Compare previous acquired weather data with current one and it sends \
       an email in case the difference between each is \
       grater than threshold values.

    1. Configure logging system
    2. Read configuration file
    3. Read current values: town, temperature, and humidity
    4. Compare previous data with current data (temperature and humidity)
    5. Update town, temperature, and humidity in configuration file
    6. Send an email if the difference between previous and current weather \
      data is greater than threshold values
    """
    if getCommandLineArgument('h', 'help'):
        print(getHelper())
        exit()

    ConfigLogs()

    configData = ConfigReader('client').configData

    emailReceiver = configData['email']
    tempThreshold = configData['tempThreshold']
    humidityThreshold = configData['humidityThreshold']
    prevTown = configData['town']
    prevTemp = configData['temp']
    prevHumidity = configData['humidity']

    currTown, currTemp, currHumidity = getWeatherData()
    if not currTown or not currTemp or not currHumidity:
        logging.exception('Verify town, temperature, and humidity is set \
into configuration file')
        exit()

    emailMessage = ''
    if prevTown == currTown:
        if abs(prevTemp - currTemp) > tempThreshold:
            emailMessage += f'A difference in temperature greater than \
{tempThreshold} was identified for {currTown}\n'
        if abs(prevHumidity - currHumidity) > humidityThreshold:
            emailMessage += f'A difference in humidity greater than \
{humidityThreshold} was identified for {currTown}\n'
    else:
        emailMessage = f'First data for {currTown} \
temp: {currTemp} and humidity: {currHumidity}'

    configWriter = ConfigWriter('client')
    configWriter.clientConfig(emailReceiver, tempThreshold, humidityThreshold,
                              currTown, currTemp, currHumidity)
    configWriter.writeConfigFile()

    if emailMessage:
        logging.debug(emailMessage)
        SendEmail(emailReceiver, emailMessage)


if __name__ == '__main__':
    client()
