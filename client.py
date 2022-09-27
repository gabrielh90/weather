import logging
import os

from emailsender.EmailSender import SendEmail
from helper.ConfigReader import ConfigReader
from helper.ConfigWriter import ConfigWriter
from helper.WeatherData import getWeatherData

def client():
  """ Compares previous acquired weather data with current one and it sends an email in case the difference between each is grater than threshold values
  
    1. Configure logging system
    2. Read configuration file
    3. Read current values: town, temperature, and humidity
    4. Compare previous data with current data (temperature and humidity)
    5. Update town, temperature, and humidity in configuration file
    6. Send an email if the difference between previous and current weather data is greater than threshold values
  """

  log_dir = '/var/log/weatherclient.log'

  logging.basicConfig(filename=log_dir, 
                      level=logging.WARNING,
                      filemode='a',
                      format='%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

  configData = ConfigReader('client').configData
  
  emailReceiver = configData['email']
  tempThreshold = configData['tempthreshold']
  humidityThreshold = configData['humiditythreshold']
  prevTown = configData['town']
  prevTemp = configData['temp']
  prevHumidity = configData['humidity']

  if emailReceiver == None: # and (not tempThreshold or not humidityThreshold):
    logging.exception('Verify email is set into configuration file')
    exit()

  currTown, currTemp, currHumidity = getWeatherData()
  if not currTown or not currTemp or not currHumidity:
    logging.exception('Verify town, temperature, and humidity is set into configuration file')
    exit()


  emailMessage = ''
  if prevTown == currTown:
    if abs(prevTemp - currTemp) > tempThreshold:
      emailMessage += f'Am identificat o diferenta de temperatura mai mare de {tempThreshold} pentru orasul {currTown}\n'
    if abs(prevHumidity - currHumidity) > humidityThreshold:
      emailMessage += f'Am identificat o diferenta de umiditate mai mare de {humidityThreshold} pentru orasul {currTown}'
  else:
    emailMessage = f'Prima prelevare pentru {currTown} avand temp: {currTemp} si humidity: {currHumidity}'


  configWriter = ConfigWriter('client')
  configWriter.clientConfig(emailReceiver, tempThreshold, humidityThreshold, currTown, currTemp, currHumidity)
  configWriter.writeConfigFile()


  if emailMessage:
    print(emailMessage)
    SendEmail(emailReceiver, emailMessage)

if __name__ == '__main__':
  client()