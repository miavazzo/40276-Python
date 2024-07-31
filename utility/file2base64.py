import base64

file_path = 'C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. 40276 parametri email portale clienti - fatture Newatt\Form-Argon-Design-Form.pdf'
with open(file_path, 'rb') as file:
    encoded_string = base64.b64encode(file.read()).decode('utf-8')
    print(encoded_string)
