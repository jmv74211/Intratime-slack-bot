
import requests
from http import HTTPStatus

from lib import global_vars

DEBUG = 'DEBUG'
INFO = 'INFO'
ERROR = 'ERROR'
CRITICAL = 'CRITICAL'


def log(service_name, function, log_type, message):
    """
    Create a log message, sending a request to logger service.

    Paramters
    ---------
    service_name :str
        Service name which register the log
    function: str
        Function name which register the log
    log_type: str
        [DEBUG, INFO, ERROR, CRITICAL]
    message :str
        Log message

    Returns
    -------
    boolean:
        True if request has been received successfully, False otherwise
    """
    payload = {'service': service_name, 'function': function, 'type': log_type, 'message': message}
    headers = {'content-type': 'application/json'}

    request = requests.post(f"{global_vars.LOGGER_SERVICE_URL}/log", json=payload, headers=headers)

    return request.status_code == HTTPStatus.OK
