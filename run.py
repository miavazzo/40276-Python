'''
file per startare l'applicazione
'''
import os
from dotenv import load_dotenv
from app import create_app

# Carica le variabili d'ambiente dal file .env
load_dotenv()

config_name = os.getenv('FLASK_ENV') or 'development'
app = create_app(config_name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
