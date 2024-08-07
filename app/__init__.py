'''
Inizialization script for the app
'''
from flask import Flask
from .config import config_by_name
from .routes import bp as routes_bp

def create_app(config_name):
    '''
    parte di avvio dell'applicazione
    '''
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.register_blueprint(routes_bp, url_prefix='/')

    return app


