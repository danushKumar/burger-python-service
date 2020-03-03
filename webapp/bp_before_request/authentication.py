from flask import request, g
from markupsafe import escape
from webapp.transaction.connection_manager import get_connection
from webapp.common.app_exception import AppException
from webapp.common.app_errocode import AppErrorCode
from webapp.service import authentication_service as auth_service
from mysql.connector import Error as sql_error

def input_validator():

    if request.method == 'POST':
        data = request.get_json()

        sanitized_data = {
            "user_name": escape(data['user_name']),
            "password": escape(data['password'])
        }

        error_codes = []

        if not len(sanitized_data['user_name'].strip()):
            error_codes.append(AppErrorCode.REQUIRED_NAME)

        if not len(sanitized_data['password'].strip()):  
            error_codes.append(AppErrorCode.REQUIRED_PASSWORD)

        if len(error_codes):
            raise AppException(error_codes)

        g.inputs = sanitized_data
    
def user_name_validator():
                
        try:
            user = auth_service.get()

            if user:
                raise AppException(AppErrorCode.INVALID_NAME)
        
        except AppException as ex:
            raise ex
