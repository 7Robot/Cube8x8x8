     ______  _____      _           _
    |___   /| ___ \    | |         | |
        / / | |_/ /___ | |__   ___ | |_
       / /  |    // _ \|  _ \ / _ \|  _|
      / /   | |\ \ (_) | |_) | (_) | |_
     /_/    |_| \_\___/|____/ \___/ \__|
                              7robot.fr

# Cube8x8x8

## Contenu :
- code des pics (18F25K80)
- scripts Python pour faire fonctionner le cube !

## Organisation des trames :

### PC → PIC maitre
A full chain of bytes is sent for every color of every led of every PIC:
```text
2 bytes (PIC 0, level 0) ... 2 bytes (PIC 7, level 0)
2 bytes (PIC 0, level 1) ... 2 bytes (PIC 7, level 1)
                         ...
2 bytes (PIC 0, level 7) ... 2 bytes (PIC 7, level 7)
```
Every couple of bytes is made of 8 bits for the blue color followed with 8 bits for the red color


### PIC maitre → bus de PICs esclaves
```text
disable level 7
send 2 bytes (PIC 0, étage 0) ... 2 bytes (PIC 7, étage 0)
enable level 0
wait a few milliseconds

disable level 0
send 2 bytes (PIC 0, étage 1) ... 2 bytes (PIC 7, étage 1)
enable level 1
wait a few milliseconds

                              ...

disable level 6
send 2 bytes (PIC 0, étage 7) ... 2 bytes (PIC 7, étage 7)
enable level 7
wait a few milliseconds
```

### Par PIC esclave :
Every byte is received by every PIC but only the usefull ones are used

# Installation

Voir [scripts_python/README.md](scripts_python%2FREADME.md) pour l'installation des scripts Python
