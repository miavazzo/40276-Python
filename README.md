# Email API Project

Questa è una semplice API Flask per inviare email con o senza allegati utilizzando Microsoft Graph API.

## Setup

1. Crea un ambiente virtuale:
   ```sh
   python -m venv venv


il file api_service.exe è il servizio Windows che implementa l'API creata fra Argon e office365 per inviare posta elettronica mediante autenticazione
OAuth2 utilizzando le credenziali fornite da +Energia.

il file di log del servizio, che si trova inoltre installato nei servizi Windows, si trova in e:\progetti\email_api_oauth2 e si chiama api_debug.log

E' possibile verificare se il servizio si trova in ascolto con il seguente comando da una finestra MS-DOS:

netstat -ant | findstr 5000
  TCP    0.0.0.0:5000           0.0.0.0:0              LISTENING       InHost
  
Dopo l'installazione del servizio in windows è necessario avviare powershell con i diritti di amministratore e lanciare il seguente comando:

[Environment]::SetEnvironmentVariable("APP_API_KEY", "v4LkxIBbEHZcQT9CAvjyiA", "Machine")

Dopodichè riavviare il servizio dal pannello servizi di Windows.