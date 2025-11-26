@echo off
title Installation et Test Keylogger
color 0A

echo ========================================================
echo      INITIALISATION DU TEST KEYLOGGER (WINDOWS)
echo ========================================================

:: 1. Vérification de Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERREUR] Python n'est pas detecte !
    echo Veuillez installer Python depuis le Microsoft Store ou python.org
    echo et cochez bien "ADD TO PATH".
    pause
    exit
)

:: 2. Installation de pynput (la librairie magique pour Windows)
echo.
echo [ETAPE 1] Installation de la librairie de hook...
pip install pynput

:: 3. Lancement du script
echo.
echo [ETAPE 2] Lancement du Keylogger...
echo Tapez du texte n'importe ou (Bloc-notes, Chrome...).
echo Regardez le fichier 'keylogs.txt' apparaitre.
echo.

python keylogger_windows.py

pause
