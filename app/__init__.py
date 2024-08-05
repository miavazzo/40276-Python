'''
Inizialization script for the app
'''
from flask import Flask
from .config import Config
from .routes import bp as routes_bp

def create_app():
    '''
    parte di avvio dell'applicazione
    '''
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(routes_bp, url_prefix='/')

    return app


