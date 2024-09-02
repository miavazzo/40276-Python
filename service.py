import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import logging
import os
from dotenv import load_dotenv
from app import create_app

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

    def setup_logging(self):
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'service.log')
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

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
            load_dotenv()  # Carica le variabili d'ambiente
            app = create_app()
            env = os.getenv('FLASK_ENV', 'production')  # Default a 'production' se non specificato
            if env == 'production':
                from waitress import serve
                logging.info("Starting the application with Waitress...")
                serve(app, host='0.0.0.0', port=5000)
            else:
                logging.info("Starting the application with Flask development server...")
                app.run(host='0.0.0.0', port=5000)
        except Exception as e:
            logging.error(f"Error in main: {str(e)}")
            self.SvcStop()  # Ferma il servizio in caso di errore

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ArgonO365EmailAPIService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ArgonO365EmailAPIService)