#!/usr/bin/env python 
# -*- coding: utf8 -*-

"""
home.py
 ______  _____      _           _
|___   || ___ \    | |         | |
    / / | |_/ /___ | |__   ___ | |_
   / /  |    // _ \|  _ \ / _ \|  _|
  / /   | |\ \ (_) | |_) | (_) | |_
 /_/    |_| \_\___/|____/ \___/ \__|
			7robot.fr

Cube8x8x8

Created by Robin Beilvert
"""

# ~~~~~~~~~~~~~~~~~~~ Librairies ~~~~~~~~~~~~~~~~~~~

import sys
import os	

# Bibliothèque pour interface graphique
try:
	# for Python2
	from Tkinter import *
except ImportError:
	# for Python3
	from tkinter import *

def Touche(event):
	# On récupère la touche pressée
	touche = event.keysym
	if (touche=='Escape'):
		Mafenetre.destroy()

def Open_display_commands():
	Mafenetre.destroy()		
	os.chdir('DisplayCommands/')
	os.system('python display_commands.py')

def Open_snake():
	Mafenetre.destroy()		
	os.chdir('Snake3D/')
	os.system('python snake.py')

def Open_space_defender():
	Mafenetre.destroy()		
	os.chdir('SpaceDefender/')
	os.system('python space_defender.py')

# ~~~~~~~~~~~ Création de la fenêtre principale ~~~~~~~~~~~~~~

Mafenetre = Tk()
Mafenetre.title('Home page')
# Petite indication de la marche à suivre
SelectHint = Label(Mafenetre, text="Sélectionner le programme à exécuter :", anchor=NW , justify=LEFT)
SelectHint.grid(row=0, columnspan=3, padx = 5)

# ~~~~~~~~~~~~~~~~~~~ Boutons de lancement ~~~~~~~~~~~~~~~~~~~

# Interface de commande du cube
Button(Mafenetre, text ='Interface de commande', command = Open_display_commands).grid(row=1, column=0, padx=5, pady=5)
# Snake3D
Button(Mafenetre, text ='Snake 3D', command = Open_snake).grid(row=1, column=1, padx=5, pady=5)
# Space Defender
Button(Mafenetre, text ='Space Defender', command = Open_space_defender).grid(row=1, column=2, padx=5, pady=5)

# Un appui sur le clavier appelle la fonction Touche()
Mafenetre.bind('<Key>', Touche)

Mafenetre.mainloop()
