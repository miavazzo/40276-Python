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

class APIService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ArgonO365EmailAPIService"
    _svc_display_name_ = "Argon O365 Email API Service"
    _svc_description_ = "API per l'invio di email tramite Microsoft Office 365 con autenticazione OAuth2"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        # Setup logging
        logging.basicConfig(filename='E:\\progetti\\email_api_oauth2\\api_service.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        try:
            # Load environment variables
            load_dotenv()

            # Create and run the app
            app = create_app()
            logging.info("Starting the application with Waitress...")
            serve(app, host='0.0.0.0', port=5000)
        except Exception as e:
            logging.error(f"Error in main: {str(e)}", exc_info=True)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(APIService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(APIService)