from flask import g

import mysql.connector as connector
from flask import current_app

def get_connection():
    if 'connection' not in g:
        g.connection = connector.connect(**current_app.config["DATABASE"])

    return g.connection

def close_connection(conn):

    conn = g.pop('connection', None)

    if conn != None:
        conn.close()
        