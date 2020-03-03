from flask import g
from ..common.app_exception import AppException
from ..common.app_errocode import AppErrorCode

import functools

def login_required(fun):

    @functools.wraps(fun)
    def wrapper(*args, **kargs):
        if not g.user:
            raise AppException(AppErrorCode.UNAUTHENTICATED_ACCESS)

        return fun(*args, **kargs)
    
    return wrapper
    