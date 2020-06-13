from flask import Flask, jsonify, request
from http import HTTPStatus

from lib.global_vars import MESSAGE_FIELD
from lib.utils.time import get_current_date_time
from lib import global_messages
from lib.validate import validate_request_data
from config import settings

app = Flask(__name__)


@app.route('/echo', methods=['GET'])
def echo_api():
    """
    Endpoint to reply an alive message

    Response
    --------
    message:  ALIVE_MESSAGE
    status_code: 200
    """
    return jsonify({MESSAGE_FIELD: global_messages.ALIVE_MESSAGE})


@app.route('/log', methods=['POST'])
def register_log():
    """
    Endpoint to register a log in LOG_FILE

    Input data
    ----------
    service: str
        User email authentication
    function: str
        User password authentication
    message: str
        User email authentication
    type: str
        User password authentication

    Response
    --------
    - If bad input data
        message: BAD_DATA_ENTERED
        status_code: 400

    - If successfull registration
        message: SUCCESS_MESSAGE
        status_code: 200
    """
    data = request.get_json()
    required_data = ['service', 'function', 'message', 'type']

    if not validate_request_data(request_data=data, required_data=required_data):
        return jsonify({MESSAGE_FIELD: global_messages.BAD_DATA_MESSAGE}), HTTPStatus.BAD_REQUEST

    date_time = get_current_date_time()

    log = f"{date_time} - {data['service']} - {data['function']} - {data['type']} - {data['message']}\n"

    with open(settings.LOG_FILE, 'a') as log_file:
        log_file.write(log)

    return jsonify({MESSAGE_FIELD: global_messages.SUCCESS_MESSAGE}), HTTPStatus.OK


if __name__ == '__main__':
    app.run(host=settings.LOGGER_SERVICE_HOST, port=settings.LOGGER_SERVICE_PORT, debug=settings.DEBUG_MODE)
