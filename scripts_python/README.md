     ______  _____      _           _
    |___   /| ___ \    | |         | |
        / / | |_/ /___ | |__   ___ | |_
       / /  |    // _ \|  _ \ / _ \|  _|
      / /   | |\ \ (_) | |_) | (_) | |_
     /_/    |_| \_\___/|____/ \___/ \__|
                              7robot.fr

# Scripts Python

## Installation

*Testé en Python 3.11*

Avant toute chose, se placer dans le répertoire `scripts_python` au sein du terminal.

Créer un environnement virtuel pour installer des librairies spécifiques à ce projet :

```shell
python -m venv venv
```

Activer l'environnement virtuel pour que pip installe les librairies dedans et qu'elles soient disponibles dans le terminal courant :

```shell
source ./venv/bin/activate
```

Installer les paquets requis avec :

```shell
pip install -r requirements.txt
```

## Usage

- Si ce n'est pas déjà fait, activer l'environnement virtuel avec `source ./venv/bin/activate` pour avoir accès aux librairies.
- Exécuter `python home.py` pour avoir accès aux différents scripts élaborés.

## Troubleshooting

### Permission denied
```text
[Errno 13] could not open port /dev/ttyUSB0: [Errno 13] Permission denied: '/dev/ttyUSB0'
```

Give (temporary) read and write privileges to `/dev/ttyUSB0` after the cube is plugged in with:
```shell
sudo chmod 666 /dev/ttyUSB0
```
