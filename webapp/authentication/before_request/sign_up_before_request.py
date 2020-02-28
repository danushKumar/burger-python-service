from flask import request
from webapp.transaction.connection_manager import get_connection
from webapp.common.app_exception import AppException
from webapp.common.app_errocode import AppErrorCode
from mysql.connector import Error as sql_error

def validate():
    data = request.get_json()
    error_codes = []

    if not len(data['user_name'].strip()):
        error_codes.append(AppErrorCode.INVALID_NAME)

    if not len(data['password'].strip()):  
        error_codes.append(AppErrorCode.INVALID_PASSWORD)
    
    if len(error_codes):
        raise AppException(error_codes)

    statement = '''
                   SELECT user_id  
                   FROM users 
                   WHERE user_id = %s;
                '''
    try:    
        connection = get_connection()
        cursor = connection.cursor(buffered=True)        
        cursor.execute(statement, (data['user_name'],))
        
        if cursor.rowcount > 0:
            cursor.close()
            raise AppException(AppErrorCode.INVALID_NAME)

    except sql_error as e:
        cursor.close()
        raise AppException(AppErrorCode.DB_ERROR)

    finally: 
        cursor.close() 
