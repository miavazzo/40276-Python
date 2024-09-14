"""
This file contains the service definition for the Argon O365 Email API Service.

Functions:
    __init__: Initializes the service.
    setup_logging: Initializes the logging configuration.
    load_environment: Loads environment variables from a .env file.
    SvcStop: Handles the service stop event.
    SvcDoRun: Handles the service start event.
    main: The main function of the service.
"""
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import logging
from dotenv import load_dotenv
from app import create_app
from waitress import serve
import threading

def find_dotenv():
    possible_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'),  # Stessa directory dello script su macchina di sviluppo
        r"e:\progetti\email_api_oauth2\.env"  # Percorso sulla macchina remota
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
    print(f"Loaded .env from {dotenv_path}")
else:
    print("No .env file found")

class APIService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ArgonO365EmailAPIService"
    _svc_display_name_ = "Argon O365 Email API Service"
    _svc_description_ = "API per l'invio di email tramite Microsoft Office 365 con autenticazione OAuth2"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = False
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False
        logging.info('Service is stopping.')

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.is_running = True
        self.main()

    def main(self):
        # Setup logging
        log_dir = r'e:\progetti\email_api_oauth2\logs'
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'api_service.log')
        logging.basicConfig(filename=log_file,
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        try:
            # Verifica se l'API_KEY è stata caricata
            api_key = os.getenv('APP_API_KEY')
            if api_key:
                logging.info("API_KEY loaded successfully")
            else:
                logging.error("Failed to load API_KEY from .env file")

            # Create the app
            app = create_app()

            # Run the app in a separate thread
            def run_server():
                logging.info("Starting the application with Waitress...")
                serve(app, host='0.0.0.0', port=5000)

            server_thread = threading.Thread(target=run_server)
            server_thread.start()

            # Main service loop
            while self.is_running:
                rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
                if rc == win32event.WAIT_OBJECT_0:
                    # Stop signal received
                    break

            logging.info("Service is shutting down.")
        except Exception as e:
            logging.error(f"Error in main: {str(e)}", exc_info=True)
        finally:
            self.is_running = False

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(APIService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(APIService)