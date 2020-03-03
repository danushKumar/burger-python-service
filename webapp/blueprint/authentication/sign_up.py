import json

from flask import Blueprint, request, g, abort, make_response, jsonify, session
from werkzeug.security import check_password_hash
from markupsafe import escape
from mysql.connector import Error as err
from mysql.connector import Error as sql_error
from webapp.common.app_exception import AppException
from webapp.common.app_errocode import AppErrorCode   
from webapp.error_handler.authentication_error_handler import error_handler
from webapp.bp_before_request.authentication import input_validator, user_name_validator
from webapp.transaction.connection_manager import get_connection
from webapp.service import authentication_service as auth_service 

bp = Blueprint('sign_up', __name__)
bp.register_error_handler(AppException, error_handler)
bp.before_request(input_validator)
bp.before_request(user_name_validator)

@bp.route('/sign-up', methods=['POST'])
def sign_up():
    # try: 
    auth_service.create()
        
    # except AppException as ex:
    #     raise ex
    
    return "success"
