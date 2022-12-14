"""Has helper functions."""
import getopt
import re
import sys


def isEmailValid(email) -> bool:
    """Validate email.

    Args:
        email (string): email to be verified

    Returns:
        bool: True - email is valid, otherwise False
    """
    pattern = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_\
`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d\
-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:\
[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]\
|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\
|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f\
]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"

    if re.match(pattern, email):
        return True
    else:
        return False


def getCommandLineArgument(shortOpt=None, longOpt=None):
    """Get command line argument.

    Args:
        shortOpt (str, optional): Short option name. Defaults to None.
        longOpt (str, optional): Long option name. Defaults to None.

    Raises:
        Exception: Function argument!
        err: GetoptError

    Returns:
        None/bool/str: option value if was given as argument otherwise value None
    """
    if not shortOpt and not longOpt:
        raise Exception('Function should be given at least one argument!')

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:v:e:s:c:k:h',
                                   ['dumpFileName=', 'verbosityLevel=',
                                    'emailCredentialsFileName=',
                                    'serverFileName=',
                                    'clientFileName=', 'key=', 'help'])
    except getopt.GetoptError as err:
        raise err
    else:
        for opt, arg in opts:
            if opt in ('-' + shortOpt, '--' + longOpt):
                if arg:
                    return arg
                else:
                    return True

    return None


def getHelper():
    """Get helper menu.

    Returns:
        str: Return helper menu
    """
    menu = ''
    menu += '-d, --dumpFileName\tLogs destination file name\n'
    menu += '-v, --verbosityLevel\tVerbosity level: debug, info and warning\n'
    menu += '-e, --emailCredentialsFileName \tEmail and Password Credentials \
file name\n'
    menu += '-s, --serverFileName\tClient Side Configuration file name\n'
    menu += '-c, --clientFileName\tClient Side Configuration file name \n'
    menu += '-k, --key\tAPI weather key\n'
    menu += '-h, --help\n'
    menu += 'Examples:\n'
    menu += 'python client.py -k 305cf38b250725bc1abc1d56c85edf88 -d \
      /home/gaby/projects/weather/weather.log -v debug --help\n'
    menu += 'python server.py -k 305cf38b250725bc1abc1d56c85edf88 -d \
      /home/gaby/projects/weather/weather.log -v debug --help\n'

    return menu


def isFloat(num):
    """Check if the given value is float.

    Args:
        value (string): value to be tested

    Returns:
        bool: True - value is float, otherwise False
    """
    try:
        float(num)
        return True
    except ValueError:
        return False
