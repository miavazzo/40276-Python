# Usa una immagine di base leggera con Python
FROM python:3.11-slim

# Imposta la directory di lavoro nel container
WORKDIR /app

# Copia il file requirements.txt nella directory di lavoro
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il resto del codice nell'immagine
COPY . .

# Espone la porta su cui l'applicazione sarà in ascolto
EXPOSE 5000

# Definisce il comando di avvio dell'applicazione
CMD ["python", "run.py"]
