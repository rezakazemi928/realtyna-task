import json

from flask import Response


def handle_error_response(
    type: str,
    code: int,
    sub_code: int,
    status: int,
    mimetype: str = "application/json",
    msg: str = None,
):
    """Handle the error response

    Args:
        type (str): error type
        code (int): error code
        sub_code (int): error sub code
        status (int): error status
        mimetype (str, optional): content type, Defaults to "application/json".
        msg (str, optional): error message. Defaults to None.

    Returns:
        str: HTTP Response
    """
    err = json.dumps({"type": type, "code": code, "subcode": sub_code, "msg": msg})
    return Response(err, status=status, mimetype=mimetype)


def write_into_file(location, content):
    with open(location, "w") as file:
        # formatted_json_str = json.dumps(paginated_date, indent=4)
        file.write(content)
