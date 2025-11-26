@echo off
title Installation et Test Keylogger (Auto)
color 0A

echo ========================================================
echo      INITIALISATION DU TEST KEYLOGGER (WINDOWS)
echo ========================================================

:: 1. Vérification de Python
echo [ETAPE 1] Verification de l'environnement...
python --version >nul 2>&1

if %errorlevel% neq 0 (
    color 0E
    echo [ALERTE] Python n'est pas detecte.
    echo [ACTION] Tentative d'installation automatique de Python 3.11...
    echo Veuillez patienter, cela peut prendre quelques minutes...
    
    :: Commande magique : Installe Python silencieusement via Winget
    winget install -e --id Python.Python.3.11 --scope machine --accept-package-agreements --accept-source-agreements >nul 2>&1
    
    :: Vérification après installation
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        color 0C
        echo [ERREUR CRITIQUE] L'installation automatique a echoue.
        echo Windows n'a pas pu installer Python. Faites-le manuellement sur python.org.
        pause
        exit
    ) else (
        color 0A
        echo [SUCCES] Python a ete installe !
    )
) else (
    echo [OK] Python est deja present.
)

:: 2. Installation de pynput
echo.
echo [ETAPE 2] Installation de la librairie de hook (pynput)...
pip install pynput >nul 2>&1

if %errorlevel% neq 0 (
    echo [INFO] Tentative de mise a jour de PIP...
    python -m pip install --upgrade pip >nul 2>&1
    pip install pynput >nul 2>&1
)

:: 3. Lancement du script
echo.
echo [ETAPE 3] Lancement du Keylogger...
echo ========================================================
echo.
echo    >>> LE KEYLOGGER ECOUTE MAINTENANT <<<
echo.
echo 1. Ouvrez le Bloc-notes ou un navigateur.
echo 2. Tapez du texte.
echo 3. Regardez les lettres s'afficher ici et dans 'keylogs.txt'.
echo.

python keylogger_windows.py

pause
