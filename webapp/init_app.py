from .transaction.connection_manager import close_connection
from flask.cli import click, with_appcontext
from webapp.transaction.connection_manager import get_connection, close_connection
from  mysql.connector import errorcode
from flask import current_app

import mysql.connector as connector 

def init_app(app):
    app.cli.add_command(init_db)
    app.teardown_appcontext(close_connection)

@click.command('init-db')
@with_appcontext
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    with current_app.open_resource('./transaction/assets/initialize_database.sql', 'r') as f:
        cursor.execute(f.read())
        cursor.close()
    
    print('initialised database')
    
