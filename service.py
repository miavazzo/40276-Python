import socket
import sys
import logging
import os
import win32serviceutil
import win32service
import win32event
import servicemanager
from dotenv import load_dotenv
from app import create_app

BASE_DIR = r"E:\progetti\email_api_oauth2"

class ArgonO365EmailAPIService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ArgonO365EmailAPIService"
    _svc_display_name_ = "Argon O365 Email API Service"
    _svc_description_ = "API per l'invio di email tramite Microsoft Office 365 con autenticazione OAuth2"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_alive = True
        self.setup_logging()
        self.load_environment()

    def setup_logging(self):
        log_dir = os.path.join(BASE_DIR, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'service.log')
        
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        
    def load_environment(self):
        dotenv_path = os.path.join(BASE_DIR, '.env')
        logging.info(f"Attempting to load .env from: {dotenv_path}")
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
            logging.info(f"Loaded environment from {dotenv_path}")
            
            # Verifica esplicita per APP_API_KEY
            api_key = os.getenv('APP_API_KEY')
            if api_key:
                logging.info(f"APP_API_KEY loaded successfully. First 4 characters: {api_key[:4]}...")
            else:
                logging.error("APP_API_KEY not found in .env file")
            
            # Log di tutte le variabili d'ambiente caricate (escludi valori sensibili)
            env_vars = dict(os.environ)
            safe_env_vars = {k: v[:4] + '...' if k in ['APP_API_KEY', 'CLIENT_SECRET'] else v for k, v in env_vars.items()}
            logging.debug(f"Loaded environment variables: {safe_env_vars}")
        else:
            logging.error(f".env file not found at {dotenv_path}")

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False
        logging.info("Service is stopping.")

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        logging.info("Service is starting.")
        try:
            app = create_app()
            
            # Verifica aggiuntiva per APP_API_KEY
            if 'API_KEY' not in app.config or not app.config['API_KEY']:
                logging.error("APP_API_KEY not found in app configuration")
                raise ValueError("APP_API_KEY not set")
            
            env = os.getenv('FLASK_ENV', 'production')
            logging.info(f"Running in {env} mode")
            if env == 'production':
                from waitress import serve
                logging.info("Starting the application with Waitress...")
                serve(app, host='0.0.0.0', port=5000)
            else:
                logging.info("Starting the application with Flask development server...")
                app.run(host='0.0.0.0', port=5000)
        except Exception as e:
            logging.error(f"Error in main: {str(e)}")
            self.SvcStop()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ArgonO365EmailAPIService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ArgonO365EmailAPIService)