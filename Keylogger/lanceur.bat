@echo off
title INSTALLATION ET LANCEMENT (V2)
color 0B

echo.
echo ======================================================
echo   INSTALLATION ROBUSTE (CORRECTION PIP)
echo ======================================================
echo.

:: 1. VERIFICATION PYTHON
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ALERTE] Python manquant. Installation via Winget...
    echo Cela peut prendre 2 minutes...
    winget install -e --id Python.Python.3.11 --scope machine --accept-package-agreements --accept-source-agreements
)

:: 2. INSTALLATION DES DEPENDANCES (METHODE FIABLE)
echo.
echo [ACTION] Installation de pynput via module Python...
:: On utilise 'python -m pip' au lieu de 'pip' seul pour éviter les erreurs de PATH
python -m pip install pynput --upgrade

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [ERREUR CRITIQUE] L'installation de pynput a echoue.
    echo Essayez de relancer ce script en mode Administrateur.
    pause
    exit
)

:: 3. LANCEMENT DU KEYLOGGER
echo.
echo [SUCCES] Bibliotheques installees.
echo [ACTION] Demarrage du Keylogger...
echo.
echo    >>> TAPEZ DU TEXTE MAINTENANT ! <<<
echo.

python keylogger_windows.py

pause
