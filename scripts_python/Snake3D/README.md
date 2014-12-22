Snake3D
=======

Un script python pour un snake en 3D dans un cube LED (jusqu'à 9x9x9)
Le code génère une matrice comprennant des valeurs suivantes 0 (éteint), 1 (rouge), 2 (bleu) ou 3 (violet)

Installation
=======

#### pySerial :

yaourt pyserial

=>	community/python-pyserial
    	Multiplatform Serial Port Module for Python


#### Pygame :

sudo svn co svn://seul.org/svn/pygame/trunk pygame

cd pygame
sudo python3 setup.py build
sudo python3 setup.py install