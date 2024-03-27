import json
from flask import Response

def handle_error_response(type:str, code:int, sub_code:int, status:int, mimetype:str="application/json",msg:str=None) -> str:
    err = json.dumps(
        {
            "type": type,
            "code": code,
            "subcode": sub_code,
            "msg": msg
        }
    )
    return Response(err, status=status, mimetype=mimetype)