# 🛡️ Architecture Sécurisée et Analyse de Vulnérabilité : Mise en place d'un KeyLogger

#### ⚠️ AVERTISSEMENT LÉGAL ET ÉTHIQUE : 
Ce projet a été développé dans un cadre strictement académique pour le Master 2 au sein du cours  "Architecture Sécurisée et Analyse de Vulnérabilité" à l'Efrei. Il a pour but d'étudier les mécanismes de persistance, d'obfuscation et d'exfiltration utilisés par les malwares modernes. L'utilisation de ce code sur des systèmes tiers sans consentement explicite est illégale et passible de sanctions pénales.

### 📑 Sommaire

1) Architecture du Projet
2) Configuration de l'Attaquant (Kali Linux)
3) Configuration de la Cible (Windows 10/11)
4)  Scénario de Démonstration
5)   Analyse Technique des Mécanismes

#### 1. Architecture du Projet

Ce projet implémente une Kill Chain complète simulant une attaque par KeyLogger. L'architecture repose sur un modèle Client-Serveur (C2 - Command & Control) utilisant un tunnel chiffré pour traverser les pare-feux (NAT Traversal).

- Le Payload (Client) : Un exécutable Windows furtif (.exe) qui capture les frappes clavier (Keylogger), filtre les données inutiles et les stocke temporairement.
- Le Canal (Tunneling) : Utilisation de Ngrok pour exposer un service local sur Internet via HTTPS, rendant le flux difficile à distinguer du trafic légitime.
- Le C2 (Serveur) : Un serveur Python Flask hébergé sur Kali Linux qui réceptionne les données exfiltrées, les affiche en temps réel et assure leur persistance sur disque.

#### 2. Configuration de l'Attaquant (Kali Linux)

L'infrastructure serveur a été entièrement automatisée via un script Python pour garantir un déploiement rapide et sans erreur.

###### Prérequis

- Python 3 et pip.
- Bibliothèques : flask, requests.
- Outil : Ngrok (installé et authentifié avec un token).

###### Fichiers Clés

- log_receiver.py : Le cœur du serveur C2 (Flask).
- lanceur_serveur.py : Orchestrateur qui gère le tunnel Ngrok et le serveur Flask simultanément.

###### 🚀 Démarrage de l'Infrastructure

Sur la machine Kali, ouvrez un terminal dans le dossier du projet et lancer l'orchestrateur :

`python3 lanceur_serveur.py`

Fonctionnement du script :

- Il nettoie les processus fantômes (conflits de port 5000).
- Il lance Ngrok en arrière-plan.
- Il récupère automatiquement l'URL Publique HTTPS via l'API locale de Ngrok.
- Il affiche cette URL (nécessaire pour le client).
- Il lance Flask au premier plan pour afficher les logs entrants en direct.

Note : Gardez ce terminal ouvert pour voir les mots de passe capturés apparaître en temps réel.

#### 3. Configuration de la Cible (Windows 10/11)

La partie cliente consiste à transformer un script Python en un binaire autonome, en utilisant des techniques d'ingénierie sociale pour tromper la victime.

Prérequis de Compilation :

- Machine Windows avec Python 3.x.
- Dépendances : `pip install pynput requests pyinstaller`.
- Ressource : Une icône réaliste (ex: acrobat.ico) placée dans le dossier.

###### ⚙️ Création du Payload (Build)

Configuration de l'URL :
Ouvrez le fichier keylogger_win_remote.py et modifiez la variable NGROK_URL avec l'adresse fournie par l'attaquant à l'étape précédente :

`NGROK_URL = "[https://votre-url-dynamique.ngrok-free.app](https://votre-url-dynamique.ngrok-free.app)"`


Compilation Furtive :
Ouvrez l'invite de commande (CMD) dans le dossier du script et exécutez la commande suivante. Elle génère un exécutable unique, sans console, avec l'icône d'Adobe Acrobat :

`py -m PyInstaller --onefile --noconsole --hidden-import pynput --icon=acrobat.ico --clean Reader_install.py`


**--onefile :** Package tout (Python, libs, script) dans un seul .exe.

**--noconsole :** Mode Silencieux. Aucune fenêtre ne s'ouvre au lancement.

**--icon=acrobat.ico :** Spoofing. L'exécutable ressemble à un installeur officiel.

**Récupération :**
Le fichier infecté se trouve dans le dossier dist/Reader_install.exe.

#### 4. Scénario de Démonstration

Pour évaluer le projet, suivez ces étapes :

**Attaquant :** Lancez `python3 lanceur_serveur.py` sur Kali. Le serveur est en écoute.

**Victime :** Sur Windows, double-cliquez sur Reader_install.exe.

**Observation :** Rien ne se passe à l'écran (comportement attendu du malware). Vérifiez le Gestionnaire des tâches pour voir le processus en arrière-plan.

**Activité :** Ouvrez un Bloc-notes et tapez du texte, des mots de passe. Vous pouvez aussi saisir du texte dans le navigateur par exemple.

**Exfiltration :** Appuyez sur ENTRÉE pour forcer l'envoi immédiat. Ou patientez 60 secondes (cycle automatique).

**Résultat :** Sur le terminal Kali, vous verrez apparaître :

`[+] Log reçu : MonMotDePasseSecret123`


Les données sont également archivées dans logs_exfiltres_recus.txt.

#### 5. Analyse Technique des Mécanismes

Ce projet démontre plusieurs concepts avancés de développement de malware :

###### A. Fiabilité de l'Exfiltration (TCP/HTTP)

Le client n'envoie pas les données "à l'aveugle". Il implémente une logique de confirmation de réception :
Le buffer local contenant les frappes n'est vidé QUE SI le serveur répond avec un code HTTP 200 OK.
Si la connexion est coupée, le keylogger continue d'enregistrer localement. Les données accumulées seront envoyées en bloc dès le rétablissement de la connexion.

###### B. Optimisation des Données

Pour éviter de "spammer" le serveur C2 avec des logs illisibles :

**Filtrage :** Les touches de contrôle (CTRL, ALT, SHIFT) sont interceptées mais ignorées pour ne garder que le texte utile.


###### C. Persistance et Discrétion

Backup Local : En cas d'échec critique du réseau, une copie des logs est écrite discrètement dans le répertoire temporaire de l'utilisateur (%TEMP%\win_backup.log), permettant une récupération physique ultérieure (Forensics).

**Processus Arrière-plan :** L'utilisation de pythonw (via PyInstaller --noconsole) détache le processus de la console standard Windows.
