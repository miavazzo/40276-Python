import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
from app import create_app  # Assicurati di importare correttamente la tua applicazione Flask da run.py

class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "ArgonOAuth2APIService"
    _svc_display_name_ = "API Argon OAuth2 Office365"
    _svc_description_ = "API per l'invio di email tramite Microsoft office365 con autenticazione OAuth2"

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
        app = create_app()  # Crea l'applicazione Flask
        app.run()  # Avvia l'applicazione Flask

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)