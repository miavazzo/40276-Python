'''
file per startare l'applicazione
'''
import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()

app = create_app()

if __name__ == "__main__":
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        from waitress import serve
        print("Starting the application with Waitress...")
        serve(app, host='0.0.0.0', port=5000)
    else:
        print("Starting the application with Flask development server...")
        app.run(host='0.0.0.0', port=5000)
