
def validate_request_data(request_data, required_data):
    """
    Validate a request data

    Parameters
    ----------
    request_data: dict
        Request response result
    required_data: list
        List of required data

    Returns
    -------
    boolean:
        True if successfull validation, False otherwise
    """
    if request_data is None:
        return False

    for item in required_data:
        if item not in request_data:
            return False

    return True
