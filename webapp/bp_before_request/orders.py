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
            'meat': escape(data['meat']),
            'bacon': escape(data['bacon']),
            'cheese': escape(data['cheese']),
            'salad': escape(data['salad']),
            'total_cost': escape(data['total_cost'])
        }

        total_add_ons = 0

        try:
            for key, value in sanitized_data.items():
                if not key == 'total_cost':
                    total_add_ons += int(value)
                    
        except ValueError as e:
            raise AppException(AppErrorCode.INVALID_DATA)

        if not total_add_ons:
            raise AppException(AppErrorCode.ZERO_ADD_ONS)

        g.inputs = sanitized_data
