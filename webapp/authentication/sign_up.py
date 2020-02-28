from flask import Blueprint, request, g, abort, make_response, jsonify
from markupsafe import escape
from ..transaction.connection_manager import get_connection
from ..common.app_exception import AppException
from ..common.app_errocode import AppErrorCode   
from .error_handler.sign_up_error_handler import error_handler
from mysql.connector import Error as err
from .before_request.sign_up_before_request import validate
from mysql.connector import Error as sql_error
import json

bp = Blueprint('sign_up', __name__)
bp.register_error_handler(AppException, error_handler)
bp.before_request(validate)

@bp.route('/sign-up', methods=['POST'])
def sign_up():
    json_data = request.get_json()
    
    statement = '''INSERT INTO burger_builder.users(user_id, password) 
                   VALUES (%s, %s);
                '''

    user_name = escape(json_data['user_name'])
    password = escape(json_data['password'])

    try: 
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(statement, (user_name, password))
        connection.commit()
        cursor.close()

    except sql_error as e:
        connection.rollback()
        raise AppException([AppErrorCode.DB_ERROR], e)

    finally:
        cursor.close()
    
    return "success"


        