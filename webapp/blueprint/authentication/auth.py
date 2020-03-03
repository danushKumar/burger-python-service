import json

from flask import Blueprint, request, g, abort, make_response, jsonify, session
from werkzeug.security import check_password_hash
from markupsafe import escape
from mysql.connector import Error as err
from mysql.connector import Error as sql_error
from webapp.common.app_exception import AppException
from webapp.common.app_errocode import AppErrorCode   
from webapp.error_handler.authentication_error_handler import error_handler
from webapp.transaction.connection_manager import get_connection
from webapp.service import authentication_service as auth_service
from webapp.bp_before_request.authentication import input_validator

bp = Blueprint('auth', __name__, url_prefix='/auth')
bp.register_error_handler(AppException, error_handler)
bp.before_request(input_validator)

@bp.route('/login', methods=['POST'])
def login():
    # try: 
    user = auth_service.get()

    if not user:
        raise AppException(AppErrorCode.UNREGISTERED_USER)

    if not check_password_hash(user[2], g.inputs['password']):
        raise AppException(AppErrorCode.INVALID_PASSWORD)        
        
    session['user'] = user

    # except AppException as ex:
    #     raise ex
    
    return "login"  

@bp.route('/logout', methods=['GET'])
def log_out():
    session.pop('user', None)
    
    return 'logged out'
     