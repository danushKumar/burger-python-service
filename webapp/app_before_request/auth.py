from flask import session, g

def auth_validator():

    g.user = session.get('user', None)
    