'''
dependendies import section
'''
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    '''
    configuration file for the app
    '''
    SECRET_KEY = os.getenv('SECRET_KEY') #os.environ.get('SECRET_KEY', 'default_secret_key')
    CLIENT_ID = os.getenv('CLIENT_IDS') #os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET') #os.environ.get('CLIENT_SECRET')
    TENANT_ID = os.getenv('TENANT_IDS') #os.environ.get('TENANT_ID')
    USERNAME = os.getenv('APP_USERNAME') #os.environ.get('USERNAME')
    API_KEY = os.getenv('APP_API_KEY') #os.environ.get('API_KEY')
