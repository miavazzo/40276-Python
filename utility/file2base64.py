import base64

# Codifica e salva il primo file
file_path = r'C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. 40276 parametri email portale clienti - fatture Newatt\Form-Argon-Design-Form.pdf'
with open(file_path, 'rb') as file:
    encoded_string = base64.b64encode(file.read()).decode('utf-8')
    with open('encoded_form_argon_design_form.txt', 'w') as output_file:
        output_file.write(encoded_string)

print("La stringa Base64 per il primo file è stata salvata in 'encoded_form_argon_design_form.txt'.")
input("Premi Enter per continuare...")

# Codifica e salva il secondo file
file_path = r'C:\Users\miavazzo\OneDrive - Capgemini\Documents\T. 40276 parametri email portale clienti - fatture Newatt\Crypto101.pdf'
with open(file_path, 'rb') as file:
    encoded_string = base64.b64encode(file.read()).decode('utf-8')
    with open('encoded_crypto101.txt', 'w') as output_file:
        output_file.write(encoded_string)

print("La stringa Base64 per il secondo file è stata salvata in 'encoded_crypto101.txt'.")
