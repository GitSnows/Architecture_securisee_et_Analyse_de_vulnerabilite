@echo off
title Keylogger Simple - Preuve de Concept

echo [1] Verification des librairies...
pip install pynput

if %errorlevel% neq 0 (
    echo [ERREUR] Installation pynput a echoue. Verifiez Python et le PATH.
    pause
    exit
)

echo [2] Lancement du Keylogger...
python simple_keylogger.py

pause
