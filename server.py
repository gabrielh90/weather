import logging
from helper.API import API
from helper.ConfigReader import ConfigReader
from helper.WeatherData import setWeatherData

def server():
  """ Gets weather from an API and logs the gathered data into a file

    1. Configure logging system
    2. Read configuration file
    3. Make API request
    4. Write gathered data to file
  """
  log_dir = '/var/log/weatherserver.log'

  logging.basicConfig(filename=log_dir, 
                      level=logging.WARNING,
                      filemode='a',
                      format='%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

  configRead = ConfigReader()
  town = configRead.configData['town']

  api = API(town)
  if api.weatherForecast['temp'] is None or api.weatherForecast['humidity'] is None :
    logging.error('Could not collect the temperature and humidity!')
    exit()

  setWeatherData(api.weatherForecast)

if __name__ == '__main__':
  server()
