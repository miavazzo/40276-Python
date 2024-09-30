import shutil
import zipfile
import os
from datetime import datetime

def archive_log(log_path, archive_dir):
    # Crea il nome del file di archivio
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"log_archive_{timestamp}.zip"
    archive_path = os.path.join(archive_dir, archive_name)

    # Copia il contenuto del file di log
    with open(log_path, 'r') as log_file:
        log_content = log_file.read()

    # Crea un file ZIP e aggiungi il contenuto del log
    with zipfile.ZipFile(archive_path, 'w') as zip_file:
        zip_file.writestr("archived_log.log", log_content)

    # Svuota il file di log originale
    open(log_path, 'w').close()

    print(f"Log archiviato in: {archive_path}")

def main():
    log_file_path = r"E:\progetti\email_api_oauth2\api_debug.log"
    archive_directory = r"E:\progetti\email_api_oauth2\logs"
    
    archive_log(log_file_path, archive_directory)

if __name__ == "__main__":
    main()