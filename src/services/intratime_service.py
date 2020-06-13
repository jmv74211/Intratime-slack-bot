from flask import Flask, jsonify, request
import json
import requests
from http import HTTPStatus


from config import settings
from lib.global_vars import MESSAGE_FIELD
from lib.validate import validate_request_data
from lib import global_messages, intratime, codes, logger


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
    return jsonify({MESSAGE_FIELD: global_messages.ALIVE_MESSAGE}), HTTPStatus.OK


@app.route('/check_user_credentials', methods=['GET'])
def check_credentials():
    """
    Endpoint to validate user credentials

    Input data
    ----------
    email: str
        User email authentication
    passsword: str
        User password authentication

    Response
    --------
    - If successful authentication
        message:  SUCCESS_MESSAGE
        status_code: 200

    - If failed authentication
        message: BAD_AUTH_DATA
        status_code: 401

    - If bad input data
        message: BAD_DATA_ENTERED
        status_code: 400
    """
    data = request.get_json()
    required_data = ['email', 'password']

    if not validate_request_data(request_data=data, required_data=required_data):
        logger.log(service_name=settings.INTRATIME_SERVICE_NAME, function=check_credentials.__name__,
                   log_type=logger.ERROR, message=global_messages.BAD_DATA_ENTERED)
        return jsonify({MESSAGE_FIELD: global_messages.BAD_DATA_MESSAGE}), HTTPStatus.BAD_REQUEST

    credentials_ok = intratime.check_user_credentials(email=data['email'], password=data['password'])

    if not credentials_ok:
        logger.log(service_name=settings.INTRATIME_SERVICE_NAME, function=check_credentials.__name__,
                   log_type=logger.DEBUG, message=global_messages.BAD_AUTH_DATA)
        return jsonify({MESSAGE_FIELD: global_messages.WRONG_CREDENTIALS_MESSAGE}), HTTPStatus.UNAUTHORIZED

    return jsonify({MESSAGE_FIELD: global_messages.SUCCESS_MESSAGE}), HTTPStatus.OK


@app.route('/register', methods=['POST'])
def register():
    """
    Endpoint to perform an intratime API registration

    Input data
    ----------
    email: str
        User email authentication
    passsword: str
        User password authentication

    Response
    --------
    - If successful registration
        message:  SUCCESS_MESSAGE
        status_code: 200

    - If failed authentication
        message: BAD_AUTH_DATA
        status_code: 401

    - If bad input data
        message: BAD_DATA_ENTERED
        status_code: 400

    - If intratime API connection error
        message: INTRATIME_CONNECT_ERROR_MESSAGE
        status_code: 500
    """
    data = request.get_json()
    required_data = ['email', 'password', 'action']

    if not validate_request_data(request_data=data, required_data=required_data):
        logger.log(service_name=settings.INTRATIME_SERVICE_NAME, function=register.__name__,
                   log_type=logger.ERROR, message=global_messages.BAD_DATA_ENTERED)
        return jsonify({MESSAGE_FIELD: global_messages.BAD_DATA_MESSAGE}), HTTPStatus.BAD_REQUEST

    token = intratime.get_login_token(email=data['email'], password=data['password'])

    if token == codes.INTRATIME_AUTH_ERROR:
        logger.log(service_name=settings.INTRATIME_SERVICE_NAME, function=register.__name__,
                   log_type=logger.DEBUG, message=global_messages.BAD_AUTH_DATA)
        return jsonify({MESSAGE_FIELD: global_messages.WRONG_CREDENTIALS_MESSAGE}), HTTPStatus.UNAUTHORIZED

    elif token == codes.INTRATIME_API_CONNECTION_ERROR:
        logger.log(service_name=settings.INTRATIME_SERVICE_NAME, function=register.__name__,
                   log_type=logger.ERROR, message=global_messages.BAD_AUTH_DATA)
        return jsonify({MESSAGE_FIELD: global_messages.INTRATIME_CONNECT_ERROR_MESSAGE}),\
            HTTPStatus.INTERNAL_SERVER_ERROR

    register_status = intratime.clocking(action=data['action'], token=token, email=data['email'])

    if register_status == codes.INTRATIME_AUTH_ERROR:
        logger.log(service_name=settings.INTRATIME_SERVICE_NAME, function=register.__name__,
                   log_type=logger.ERROR, message=global_messages.BAD_AUTH_DATA)
        return jsonify({MESSAGE_FIELD: global_messages.FAIL_INTRATIME_REGISTER_MESSAGE}), HTTPStatus.UNAUTHORIZED

    elif register_status == codes.INTRATIME_API_CONNECTION_ERROR:
        logger.log(service_name=settings.INTRATIME_SERVICE_NAME, function=register.__name__,
                   log_type=logger.ERROR, message=global_messages.BAD_AUTH_DATA)
        return jsonify({MESSAGE_FIELD: global_messages.INTRATIME_CONNECT_ERROR_MESSAGE}),\
            HTTPStatus.INTERNAL_SERVER_ERROR

    return jsonify({MESSAGE_FIELD: global_messages.SUCCESS_MESSAGE}), HTTPStatus.OK


if __name__ == '__main__':
    app.run(host=settings.INTRATIME_SERVICE_HOST, port=settings.INTRATIME_SERVICE_PORT, debug=settings.DEBUG_MODE)
