# Architecture_securisee_et_Analyse_de_vulnerabilite

I. Partie Client : Keylogger Windows Furtif
Le keylogger est basé sur le script Python keylogger_win_remote.py qui a été transformé en un exécutable autonome (.exe) pour une portabilité maximale.

1. Structure du Binaire (keylogger_win_remote.exe)
L'exécutable est généré à partir du script Python via PyInstaller avec les arguments suivants :

py -m PyInstaller --onefile --noconsole --hidden-import pynput --clean keylogger_win_remote.py
--onefile : Intègre toutes les dépendances dans un seul fichier binaire, ne nécessitant aucune installation de Python ou de bibliothèques sur la machine cible.
--noconsole : Rend l'application furtive. Elle s'exécute en arrière-plan sans afficher de fenêtre de console (cmd), empêchant l'utilisateur de remarquer son activité.

Autonomie : Le .exe intègre toutes les bibliothèques nécessaires (pynput pour la capture, requests pour l'envoi HTTP) et peut être exécuté sur un poste Windows "vierge".

2. Mécanismes de Capture et de Stockage
Capture : La bibliothèque pynput est utilisée pour mettre en place un hook au niveau du système d'exploitation et intercepter les événements de clavier (frappes normales, [ENTER], [TAB], etc.).
Sauvegarde Locale (win_backup.log) : Pour assurer la persistance des données même sans connexion Internet, le script enregistre une copie de toutes les frappes dans un fichier de log local.
Emplacement : Le log est dissimulé dans le répertoire temporaire de Windows (accessible via %temp%) sous le nom de win_backup.log.

II. 📡 Partie Serveur : Réception et Exfiltration de Logs (Kali)
Le serveur d'écoute est hébergé sur la VM Kali Attaquante et utilise un tunnel sécurisé pour recevoir les données du client Windows.

1. Tunneling Sécurisé avec Ngrok
Ngrok est utilisé pour créer un tunnel sécurisé entre la VM Kali (un environnement local) et le réseau Internet public.

Rôle de Ngrok : Il expose l'interface Web locale de Flask (le port 5000) à une URL publique chiffrée (HTTPS), permettant au client Windows de se connecter de manière fiable et discrète.

Mise en place : Ngrok doit être lancé sur Kali avant de démarrer le serveur Flask, généralement pour exposer le port 5000 :
ngrok http 5000

2. Script de Réception avec Flask (log_receiver.py)
Le serveur est géré par une micro-application Web Flask en Python.
Endpoint de Réception : Le script implémente une route /log qui accepte uniquement les requêtes POST (comme un formulaire web).

Mécanisme de Flask :
Il reçoit les données des frappes envoyées par le client Windows.
Il affiche immédiatement le contenu reçu dans le terminal de la Kali pour une surveillance en temps réel.
Il enregistre de manière persistante les logs reçus dans le fichier logs_exfiltres_recus.txt sur le disque de la Kali.

3. Exfiltration Minutée
Le client Windows est configuré pour collecter les frappes et envoyer une requête HTTP POST vers l'URL Ngrok du serveur Flask à intervalles réguliers (ex: toutes les 60 secondes), ou lorsqu'un seuil de frappes est atteint.
Cette méthode permet une exfiltration par petits paquets, rendant la détection par les pare-feu plus difficile qu'une connexion longue ou constante.
