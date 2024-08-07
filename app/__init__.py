'''
Inizialization script for the app
'''
import os
from dotenv import load_dotenv
from flask import Flask
from .config import config_by_name
from .routes import bp as routes_bp

load_dotenv()

def create_app():
    '''
    parte di avvio dell'applicazione
    '''
    env = config_by_name[os.getenv('FLASK_ENV', 'development')]  # Modifica questa riga
    app = Flask(__name__)
    app.config.from_object(env)
    app.register_blueprint(routes_bp, url_prefix='/')
    return app
