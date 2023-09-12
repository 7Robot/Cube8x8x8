     ______  _____      _           _
    |___   /| ___ \    | |         | |
        / / | |_/ /___ | |__   ___ | |_
       / /  |    // _ \|  _ \ / _ \|  _|
      / /   | |\ \ (_) | |_) | (_) | |_
     /_/    |_| \_\___/|____/ \___/ \__|
                              7robot.fr

Scripts Python
================

Exécuter home.py pour avoir accès aux différents scripts élaborés.

Installation
================

#### /!\ Ne fonctionne qu'en Python 3 /!\

Paquets requis :

* Communication avec le ftdi :  
python-pylibftdi  
* Gestion de l'audio des jeux :  
python-pygame-hg  
* Gestion de l'interface graphique :  
tk

### Troubleshooting

```shell
[Errno 13] could not open port /dev/ttyUSB0: [Errno 13] Permission denied: '/dev/ttyUSB0'
```

Give read and write privileges to `/dev/ttyUSB0` after the cube is plugged in with:
```shell
sudo chmod 666 /dev/ttyUSB0
```
