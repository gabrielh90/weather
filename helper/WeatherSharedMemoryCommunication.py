"""Weather data shared memory communication."""
import json
import logging
import mmap
import os
import sys
from helper.helper import isFloat
if os.name == "nt":
    import _winapi
    _USE_POSIX = False
else:
    import _posixshmem
    _USE_POSIX = True


def setWeatherData(weatherForecast, sharedMemoryName='psm_21467_46075'):
    """Write weather data to shared memory for \
       inter applications communication.

    Args:
        weatherForecast (dictionary): town, temperature and humidity
    """
    logging.debug(f'Weather data  {weatherForecast}')
    logging.debug(f'Writing weather data in shared memory {sharedMemoryName}')

    flags = os.O_CREAT | os.O_RDWR
    if _USE_POSIX:
        sharedMemoryName = "/" + sharedMemoryName
    mode = 0o777
    try:
        fd = _posixshmem.shm_open(sharedMemoryName, flags, mode=mode)
        size = sys.getsizeof(weatherForecast)
        try:
            if size:
                os.ftruncate(fd, size)
            stats = os.fstat(fd)
            size = stats.st_size
            with mmap.mmap(fd, size) as memMap:
                memMap.write(json.dumps(weatherForecast).encode())
        except OSError as osErr:
            logging.error(osErr)
            if _USE_POSIX and sharedMemoryName:
                _posixshmem.shm_unlink(sharedMemoryName)
            raise
        except Exception as e:
            logging.error(e)
    except Exception as ex:
        logging.error(f'Unexpected error: {sharedMemoryName} is', repr(ex))
        exit()

    # _posixshmem.shm_unlink(sharedMemoryName)


def getWeatherData(sharedMemoryName='psm_21467_46075'):
    """Read weather data from shared memory for \
       inter applications communication.

    Returns:
        list: town, temperature and humidity
    """
    logging.info(f'Reading shared memory weather data {sharedMemoryName}')
    currTown = currTemp = currHumidity = None

    flags = os.O_RDONLY
    if _USE_POSIX:
        sharedMemoryName = "/" + sharedMemoryName
    # mode = 0o777
    mode = 0o600
    try:
        fd = _posixshmem.shm_open(sharedMemoryName, flags, mode=mode)
        try:
            with mmap.mmap(fileno=fd, length=0, access=mmap.ACCESS_READ)\
              as memMap:
                memMap.seek(0)
                weatherForecast = json.loads(memMap.read().decode().
                                             replace('\x00', ''))
        except OSError as osErr:
            logging.error(osErr)
            if _USE_POSIX and sharedMemoryName:
                _posixshmem.shm_unlink(sharedMemoryName)
            raise
        except Exception as e:
            logging.error(e)
        else:
            logging.info(weatherForecast)

            if 'town' in weatherForecast:
                currTown = weatherForecast['town']

            if 'temp' in weatherForecast and \
                    isFloat(weatherForecast['temp']):
                currTemp = float(weatherForecast['temp'])

            if 'humidity' in weatherForecast and \
                    isFloat(weatherForecast['humidity']):
                currHumidity = float(weatherForecast['humidity'])

    except Exception as ex:
        logging.error(f'Unexpected error: {sharedMemoryName} is', repr(ex))
        exit()

    return [currTown, currTemp, currHumidity]
