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
from webapp.service import order_service 
from webapp.bp_before_request.orders import input_validator
from webapp.utils.authentication_utils import login_required

bp = Blueprint('orders', __name__, url_prefix='/orders')
bp.register_error_handler(AppException, error_handler)
bp.before_request(input_validator)

@bp.route('/request-order', methods=['POST'])
@login_required
def request_order():
    # try: 
    order_id = order_service.create()

    # except AppException as ex:
    #     raise ex  
     
    return {
        "order_id": order_id
    }
