'''
Inizialization script for the app
'''
from flask import Flask
from .config import Config
from .routes import bp as email_bp

def create_app():
    '''
    initialize the app
    '''
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(email_bp)

    return app

