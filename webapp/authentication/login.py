from flask import Blueprint, request, g, abort, make_response, jsonify, session
from markupsafe import escape
from ..transaction.connection_manager import get_connection
from ..common.app_exception import AppException
from ..common.app_errocode import AppErrorCode   
from .error_handler.error_handler import login_error_handler
from mysql.connector import Error as err
from .before_request.sign_up_before_request import validate
from mysql.connector import Error as sql_error
import json

bp = Blueprint('login', __name__, url_prefix='/auth')
bp.register_error_handler(AppException, login_error_handler)

@bp.route('/login', methods=['POST'])
def login():
    print('hi')
    json_data = request.get_json()
    
    statement = '''
                   SELECT user_id, password 
                   FROM users 
                   WHERE user_id = %s;
                '''

    user_name = escape(json_data['user_name'])
    password = escape(json_data['password'])

    try: 
        connection = get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute(statement, (user_name,))

        if not cursor.rowcount:
            raise AppException(AppErrorCode.UNREGISTERED_USER)
        
        for row in cursor:
            g.user = row
        
        # session['user'] = g.user need to validate password
        print(session)
        cursor.close()

    except sql_error as e:
        raise AppException([AppErrorCode.DB_ERROR], e)

    finally:
        cursor.close()
    
    return "login"

@bp.before_request
def check_logged_in():

    if 'user' in session:
        g.user = session.get('user')
  

def login_required(fun):

    def wrapper(*args, **kargs):
        if not 'user' in g:
            return 'need to login'

        return fun(*args, **kargs)
    
    return wrapper

@bp.route('/loggedin', methods=['POST'])
@login_required
def logged_in():
    return 'login was successful'

@bp.route('/logout', methods=['POST'])
def logged_out():
    
    session.pop('user', None)
    print(session)
    return 'logged out'
     