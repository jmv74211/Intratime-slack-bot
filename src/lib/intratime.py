import random
import requests
import json
from http import HTTPStatus

from config import settings
from lib.utils import time
from lib import logger, global_messages, codes


INTRATIME_API_URL = 'http://newapi.intratime.es'
INTRATIME_API_LOGIN_PATH =  '/api/user/login'
INTRATIME_API_CLOCKING_PATH = f'{INTRATIME_API_URL}/api/user/clocking'
INTRATIME_API_APPLICATION_HEADER = 'Accept: application/vnd.apiintratime.v1+json'
INTRATIME_API_HEADER = {
                            'Accept': 'application/vnd.apiintratime.v1+json',
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'charset':'utf8'
                        }

def get_action(action):
    """
    Function to get the intratime action ID

    Parameters
    ----------
    action: str
        Action enum: ['in', 'out', 'pause', 'return']

    Returns
    -------
    int:
        ID associated with the action
    """
    switcher = {
        'in': 0,
        'out': 1,
        'pause': 2,
        'return': 3,
    }

    try:
        return switcher[action]
    except KeyError:
        logger.log(service_name=settings.INTRATIME_SERVICE_NAME, function=get_action.__name__, log_type=logger.ERROR,
                   message=f"Invalid '{action}' action")



def get_random_coordinates():
  """
  Function to get a random coordinates within the Wazuh office area

  Returns
  -------
  tuple:
    West and North coordinates

  """
  w = random.randint(1000,8324) # West of Greenwich meridian
  n = random.randint(5184,7163)  # North of Ecuador

  wazuh_location_w = float(f"37.147{w}")
  wazuh_location_n = float(f"-3.608{n}")

  return wazuh_location_w, wazuh_location_n


def get_login_token(email, password):
    """
    Function to get the Intratime auth token

    Parameters
    ----------
    email: str
        User authentication email
    password: str
        User authentication password

    Returns
    -------
    str:
        User session token
    int:
       codes.INTRATIME_AUTH_ERROR if user authentication has failed
       codes.INTRATIME_API_CONNECTION_ERROR if there is a Intratime API connection error
    """
    payload=f"user={email}&pin={password}"

    try:
        request = requests.post(url=f"{INTRATIME_API_URL}{INTRATIME_API_LOGIN_PATH}", data=payload,
                                headers=INTRATIME_API_HEADER)
    except ConnectionError:
        logger.log(service_name=settings.INTRATIME_SERVICE_NAME, function=get_login_token.__name__,
                   log_type=logger.ERROR, message=global_messages.INTRATIME_CONNECT_ERROR_MESSAGE)
        return codes.INTRATIME_API_CONNECTION_ERROR

    try:
        token = json.loads(request.text)['USER_TOKEN']
    except KeyError:
        logger.log(service_name=settings.INTRATIME_SERVICE_NAME, function=get_login_token.__name__,
                   log_type=logger.DEBUG, message=global_messages.INTRATIME_CONNECT_ERROR_MESSAGE)
        return codes.INTRATIME_AUTH_ERROR

    return token


def clocking(action, token, email):
    """
    Function to register an action in Intratime API

    Parameters
    ----------
    action: str
        Action enum: ['in', 'out', 'pause', 'return']
    token: str
        User session token
    email: str
        User email

    Returns
    -------
    int:
       codes.SUCCESS if clocking has been successful
       codes.INTRATIME_AUTH_ERROR if user authentication has failed
       codes.INTRATIME_API_CONNECTION_ERROR if there is a Intratime API connection error
    """
    date_time = time.get_current_date_time()

    wazuh_location_w, wazuh_location_n = get_random_coordinates()

    api_action = get_action(action)

    # Add user token to intratime header request
    INTRATIME_API_HEADER.update({ 'token': token })

    payload = f"user_action={api_action}&user_use_server_time={False}&user_timestamp={date_time}&"\
              f"user_gps_coordinates={wazuh_location_w},{wazuh_location_n}"

    try:
        request = requests.post(url=INTRATIME_API_CLOCKING_PATH, data=payload, headers=INTRATIME_API_HEADER)
        if request.status_code == HTTPStatus.CREATED:
            logger.log(service_name=settings.INTRATIME_SERVICE_NAME, function=clocking.__name__, log_type=logger.INFO,
                       message=f"The user {email} has registered {action} action")
            return codes.SUCCESS
        else:
            logger.log(service_name=settings.INTRATIME_SERVICE_NAME, function=clocking.__name__, log_type=logger.ERROR,
                       message=f"The user {email} has failed authentication")
            return codes.INTRATIME_AUTH_ERROR
    except ConnectionError:
        logger.log(service_name=settings.INTRATIME_SERVICE_NAME, function=clocking.__name__, log_type=logger.ERROR,
                   message=global_messages.INTRATIME_CONNECT_ERROR_MESSAGE)
        return codes.INTRATIME_API_CONNECTION_ERROR
