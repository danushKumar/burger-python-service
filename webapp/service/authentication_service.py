from flask import Blueprint, request, g, abort, make_response, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import escape
from ..transaction.connection_manager import get_connection
from ..common.app_exception import AppException
from ..common.app_errocode import AppErrorCode   
from mysql.connector import Error as err
from mysql.connector import Error as sql_error
import json

def create():
    statement = '''INSERT INTO users(user_id, password) 
                   VALUES (%s, %s);
                '''

    try: 
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(statement, (g.inputs['user_name'], 
                        generate_password_hash(g.inputs['password'])))
        connection.commit()
        cursor.close()

    except sql_error as e:
        connection.rollback()
        raise AppException([AppErrorCode.DB_ERROR], e)

    finally:
        cursor.close()


def get():
    statement = '''
                   SELECT id, user_id, password 
                   FROM users 
                   WHERE user_id = %s;
                '''

    try: 
        connection = get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute(statement, (g.inputs['user_name'],))

        if not cursor.rowcount:
            user = None

            return user

        for row in cursor:
            user = row

        return user

    except sql_error as e:
        raise AppException([AppErrorCode.DB_ERROR], e)

    finally:
        cursor.close()
