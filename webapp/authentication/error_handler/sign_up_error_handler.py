from flask import make_response
import json

def error_handler(e):
    cause = e.cause.__dict__ if e.cause else None
    response = make_response()
    response.data = json.dumps({
        "error_code": e.codes,
        "error_cause": cause
    })

    return response, 500
    