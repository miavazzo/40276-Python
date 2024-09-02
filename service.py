import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import logging
import os
from dotenv import load_dotenv
from run import app  # Importa l'applicazione Flask dal file run.py

class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "ArgonOAuth2APIService"
    _svc_display_name_ = "API Argon OAuth2 Office365"
    _svc_description_ = "API per l'invio di email tramite Microsoft office365 con autenticazione OAuth2"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        logging.basicConfig(
            filename='service.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
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
            env = os.getenv('FLASK_ENV', 'development')
            if env == 'production':
                from waitress import serve
                logging.info("Starting the application with Waitress...")
                serve(app, host='0.0.0.0', port=5000)
            else:
                logging.info("Starting the application with Flask development server...")
                app.run(host='0.0.0.0', port=5000)
        except Exception as e:
            logging.error(f"Error in main: {str(e)}")
            raise

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)