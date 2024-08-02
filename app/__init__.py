'''
Inizialization script for the app
'''
from flask import Flask

def create_app():
    '''
    Inizialization script for the app
    '''
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    with app.app_context():
        from . import routes
        return app
