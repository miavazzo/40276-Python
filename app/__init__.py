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
    config_name = os.getenv('FLASK_ENV', 'production')
    print(f"Starting app in {config_name} mode")  # Log
    
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])  # Usa la configurazione corretta
    app.register_blueprint(routes_bp, url_prefix='/')
    
    return app
