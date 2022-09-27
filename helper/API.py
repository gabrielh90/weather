import requests
import logging

class API():
  """Deals with weather gathering
  """

  __url = 'https://api.openweathermap.org/data/2.5/weather'

  def __init__(self, town):
    """Constructor of API class

    Args:
        town (string): The name of the town for which to gather weather data
    """
    logging.debug(f'Create API object')
    self.__town = town
    self.__weatherForecast = {
        'town': self.__town,
        'temp': None,
        'humidity': None
      }
    self.__query = {
      'appid': '305cf38b250725bc1abc1d56c85edf88',
      'q': self.__town,
      'units': 'metric',
      'lang': 'en'
    }
    self.makeRequest()

  def makeRequest(self):
    """Makes the request to chosen weather API
    """
    
    try:
      response = requests.get(self.__url, self.__query)
      response.raise_for_status()
      # Additional code will only run if the request is successful
      data = response.json()
      logging.debug(f'API request result {data}')

    except requests.exceptions.JSONDecodeError as ex:
      logging.error(ex)
    except requests.exceptions.HTTPError as ex:
      logging.error(f'HTTPError: {ex}')
    except requests.exceptions.ConnectionError as ex:
      logging.error(ex)
    except requests.exceptions.Timeout as ex:
      logging.error(ex)
    except requests.exceptions.RequestException as ex:
      logging.error(ex)
    else:
      self.__weatherForecast['temp'] = data['main']['temp']
      self.__weatherForecast['humidity'] = data['main']['humidity']

  @property
  def weatherForecast(self):
    """Access the weather API request results

    Returns:
        _type_: _description_
    """
    return self.__weatherForecast

  @weatherForecast.deleter
  def weatherForecast(self):
    """Discards the weather API request results
    """
    del self.__weatherForecast

if __name__ == '__main__':
  log_dir = '/var/log/weatherhelper.log'
  #os.chmod(log_dir, 0o777)
  logging.basicConfig(filename=log_dir, 
                      level=logging.WARNING,
                      filemode='a',
                      format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

  api = API('Burundi')