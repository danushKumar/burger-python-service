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
    statement = '''INSERT INTO order_details(meat
                                     ,bacon
                                     ,cheese
                                     ,salad
                                     ,total_cost
                                     ,user_id) 
                   VALUES (%s, %s, %s, %s, %s, %s);
                '''

    try: 
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(statement, (g.inputs['meat'], 
                                g.inputs['bacon'],
                                g.inputs['cheese'],
                                g.inputs['salad'],
                                g.inputs['total_cost'],
                                g.user[0]))
        order_id = cursor.lastrowid
        connection.commit()
        cursor.close()

        return order_id

    except sql_error as e:
        connection.rollback()
        raise AppException([AppErrorCode.DB_ERROR], e)

    finally:
        cursor.close()

def get():
    statement = '''
                   SELECT id
                         ,meat
                         ,bacon
                         ,cheese
                         ,salad
                         ,total_cost
                         ,user_id
                   FROM order_details
                   WHERE user_id = %s;
                '''

    try: 
        connection = get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute(statement, (g.user[0],))

        if not cursor.rowcount:
            orders = None

            return orders

        orders = []

        for row in cursor:
            orders.append(row)

        return orders

    except sql_error as e:
        raise AppException([AppErrorCode.DB_ERROR], e)

    finally:
        cursor.close()
