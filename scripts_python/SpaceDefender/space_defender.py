#!/usr/bin/env python 
# -*- coding: utf8 -*-

"""
space_defender.py
 ______  _____      _           _
|___   || ___ \    | |         | |
    / / | |_/ /___ | |__   ___ | |_
   / /  |    // _ \|  _ \ / _ \|  _|
  / /   | |\ \ (_) | |_) | (_) | |_
 /_/    |_| \_\___/|____/ \___/ \__|
			7robot.fr
Cube8x8x8
"""

# SPACE DEFENDER 
#
# Défendez l'espace contre l'assaut des terribles pixels bleus !
# 
# Requis : python, python-tk, pyserial
#
# Fonctionnalités :
#    * Déplacement du vaisseau
#    * Tir de missiles par le vaisseau
#    * Apparition aléatoire des attaquants
#    * Explosion des attaquants
#    * Détection des murs
#    * Différentes couleurs (vaisseau, missiles, attaquants)
#    * Un mode pause (actif au lancement)
#
# Auteur : Robin 


# ~~~~~~~~~~~~~~~~~~~ Bibliothèques ~~~~~~~~~~~~~~~~~~~

# Bibliothèques pour ftdi, calculs et gestion du temps
import sys
import os			# Permet de sauver des fichiers (scores)
from math import *
from serial import *		# Communication avec le port série 
from collections import deque 	# Permet de faires des opérations avancés sur les listes (rotate)
from random import randint    	# Permet de créer des chiffres aléatoires
from time import sleep
from pygame import mixer      	# Permet de jouer des sons

from inspect import *

# Bibliothèque pour interface graphique
try:
	# for Python2
	from Tkinter import *
except ImportError:
	# for Python3
	from tkinter import *

class Partie:

	def __init__(self):
		self.vitesse=480-4*echelle.get()
		self.nom_joueur='Anonyme'
		self.Nom_Joueur()
		self.pause=1
		self.perdu=0

	def Nom_Joueur(self):
		def Joueur(event):
			global nom_joueur

			if namefield.get() == '':
				# Nom de joueur par défaut
				self.nom_joueur='Anonyme'
			else :
				# Si le joueur a donné un nom on l'enregistre
				self.nom_joueur=namefield.get()
			Name_Screen.destroy()

				
		# Création de la fenêtre de sauvegarde
		Name_Screen = Toplevel()
		Name_Screen.title('Nom du Joueur')
		BlablaNom = Label(Name_Screen, text="Nom du joueur pour les scores :").grid()
		global namefield
		namefield= Entry(Name_Screen, textvariable="{0}".format(self.nom_joueur))
		namefield.focus_force()
		namefield.grid()
		
		# Bouton OK
		BoutonOk=Button(Name_Screen, text ='Ok')
		BoutonOk.bind("<Button-1>", Joueur)
		Name_Screen.bind("<Return>", Joueur)
		BoutonOk.grid()


class Vaisseau():

	def __init__(self):
		# Position du vaisseau, toujours dans le premier plan du cube ([etage, colonne])
		self.position=[4,3]

	def move(self,direction):	
		if (direction == 'Up'):
			self.position[0]-=1
		elif (direction == 'Down'):
			self.position[0]+=1
		elif (direction == 'Left'):
			self.position[1]-=1
		elif (direction == 'Right'):
			self.position[1]+=1

class Attaquant():
	def __init__(self):
		# Position initiale de l'attaquant dans le dernier plan du cube ([etage, ligne, colonne])
		self.position=[4,0,3]


def Touche(event):
	# Si on presse Escape on quitte la fenêtre
	if (event.keysym=='Escape'):
		Mafenetre.destroy()

	# Les touches directionnelles font bouger le vaisseau dans les limites du cube	
	if	((event.keysym=='Up' and NouveauVaisseau.position[0]>0) or 
		(event.keysym=='Down' and NouveauVaisseau.position[0]<7) or\
		(event.keysym=='Left' and NouveauVaisseau.position[1]>0) or\
		(event.keysym=='Right' and NouveauVaisseau.position[1]<7)):
			NouveauVaisseau.move(event.keysym)

	# Si on presse espace et qu'on n'a pas perdu on se met en pause ou on en sort
	if (event.keysym=='space' and NouvellePartie.perdu == 0):
		if (NouvellePartie.pause == 1):
			NouvellePartie.pause = 0
			music.play(-1)
		else:
			NouvellePartie.pause = 1
			music.stop()

# ~~~~~~~~~~~~~~~~~~~ Gestion de l'audio ~~~~~~~~~~~~~~~~~~~

# Initialize the pygame mixer
mixer.init(44100)
try:
    # Create the sound instances
    music = mixer.Sound("Sound/E1M1.wav")
    laser = mixer.Sound("Sound/laser.wav") 
    laser_fat = mixer.Sound("Sound/laser_fat.wav")

except:
    print("Error: Sound file not found")

# ~~~~~~~~~~~~~~~~~~~ Fenêtre principale ~~~~~~~~~~~~~~~~~~~
	
Mafenetre = Tk()
Mafenetre.title('Space Defender')


# Un appui sur le clavier appelle la fonction Touche() qui actualisera la direction
Mafenetre.bind('<Key>', Touche)

# Création d'un widget Scale pour la gestion de la difficulté
echelle = Scale(Mafenetre,from_=0,to=10,resolution=1,orient=HORIZONTAL,\
length=300,width=20,label="Difficulté")
# On affiche l'echelle de difficulté
echelle.grid(row=2,  column=0)

NouveauVaisseau=Vaisseau()

# Lancer une nouvelle partie
def NouvPart(event):
	global NouvellePartie
	NouvellePartie=Partie()
BoutonNouvPart= Button(Mafenetre, text = "Nouvelle Partie")
BoutonNouvPart.bind("<Button-1>", NouvPart)
Mafenetre.bind("<Return>", NouvPart)
BoutonNouvPart.grid()


Mafenetre.mainloop()

