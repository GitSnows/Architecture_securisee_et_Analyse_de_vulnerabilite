@echo off
title Keylogger Démarrage
color 0A

:: Déplace l'invite de commande dans le répertoire du script Batch
cd /d "%~dp0"

echo [1] Démarrage du Keylogger natif PowerShell...
echo [2] Veuillez autoriser l'execution du script si Windows le demande.
echo.

:: Lancement du script PowerShell : 
:: - Argument -ExecutionPolicy Bypass pour autoriser le script
:: - Utilise le chemin RELATIF du fichier (qui est maintenant valide grace au 'cd /d')
powershell.exe -ExecutionPolicy Bypass -File keylogger_ps.ps1

pause
