'''
file per startare l'applicazione
'''
from app import create_app
#from dotenv import load_dotenv
#import os

#load_dotenv()

app = create_app()

if __name__ == "__main__":
    '''
    l'applicazione ascolta su tutti gli indirizzi alla porta TCP 5000
    '''
    app.run(host='0.0.0.0', port=5000)
