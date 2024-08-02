'''
script per testare il recupero effettivo delle variabili dal file .env
'''
import os
from dotenv import load_dotenv

# Carica le variabili di ambiente dal file .env
load_dotenv()

# Recupera le variabili di ambiente
client_id = os.getenv('CLIENT_IDS')
client_secret = os.getenv('CLIENT_SECRET')
tenant_id = os.getenv('TENANT_IDS')
username = os.getenv('APP_USERNAME')
API_KEY = os.getenv('API_KEY')

print("CLIENT_ID:", client_id)
print("CLIENT_SECRET:", client_secret)
print("TENANT_ID:", tenant_id)
print("APP_USERNAME:", username)
print("API_KEY:", API_KEY)
