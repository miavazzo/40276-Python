"""
file di avvio per la nostra applicazione in produzione
"""
from app import create_app
import os

# Carica le variabili d'ambiente dal file .env
from dotenv import load_dotenv
load_dotenv()

config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)