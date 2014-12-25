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

# ~~~~~~~~~~~~~~~~~~~~~~~~ Classes ~~~~~~~~~~~~~~~~~~~~~~~~~

class Partie:

	def __init__(self):
		try:
			self.difficulty=NouvellePartie.difficulty
		except Exception:
			self.difficulty=0
		# Délai d'actualisation : 480-4*difficulty
		self.nom_joueur="Anonyme"
		self.Nom_Joueur()
		self.pause=1
		self.perdu=0
		self.niveau=0
		music.stop()

	def Nom_Joueur(self):
		def Joueur(event):
			global nom_joueur

			if namefield.get() == '':
				# Nom de joueur par défaut
				self.nom_joueur='Anonyme'
			else :
				# Si le joueur a donné un nom on l'enregistre
				self.nom_joueur=namefield.get()

			self.difficulty=echelle.get()
			global PlayerLevel
			PlayerLevel.config(text="Joueur : {0}\nDifficulté : {1}".format(self.nom_joueur,self.difficulty))
			woosh.play()
			Name_Screen.destroy()

		# Création de la fenêtre de nouvelle partie
		Name_Screen = Toplevel()
		Name_Screen.title('Nouvelle partie')

		BlablaNom = Label(Name_Screen, text="Nom du joueur :").grid(row=0, column=0, padx=6)
		namefield= Entry(Name_Screen, width=12, textvariable="{0}".format(self.nom_joueur))
		namefield.focus_force()
		namefield.grid(row=1, column=0, padx=6)
		
		# Définition de la difficulté
		echelle = Scale(Name_Screen,from_=0,to=10,resolution=1,orient=HORIZONTAL,\
		length=100,width=15, label="Difficulté :")
		echelle.set(self.difficulty)
		# On affiche l'echelle de difficulté
		echelle.grid(row=0, rowspan=2, column=1, padx=6)	

		# Bouton OK
		BoutonOk=Button(Name_Screen, text ='Ok')
		BoutonOk.bind("<Button-1>", Joueur)
		Name_Screen.bind("<Return>", Joueur)
		BoutonOk.grid(row=2, columnspan=2)

class Vaisseau():

	def __init__(self):
		# Position du vaisseau, toujours dans le premier plan du cube ([etage, colonne])
		self.position=[4,3]
		self.bonus_available=0
		self.bonus_count=0

	def move(self,direction):	
		if (direction == 'Up'):
			self.position[0]-=1
		elif (direction == 'Down'):
			self.position[0]+=1
		elif (direction == 'Left'):
			self.position[1]-=1
		elif (direction == 'Right'):
			self.position[1]+=1

	def fire(self):
		# Si des tirs bonus sont disponibles
		if (self.bonus_count>0):
			laser_fat.play()
			# On enlève un tir bonus
			self.bonus_count-=1	
		# Si on n'a pas de tir bonus en stock	
		else:
			laser.play()

	def use_bonus(self):
		# On remonte le nombre de tirs bonus disponibles
		self.bonus_count=10
		# Le bonus est utilisé, il n'est plus disponible
		self.bonus_available=0

class Attaquant():
	def __init__(self):
		# Position initiale de l'attaquant dans le dernier plan du cube ([etage, ligne, colonne])
		self.position=[4,0,3]

# ~~~~~~~~~~~~~~~~~~~~~~~ Fonctions ~~~~~~~~~~~~~~~~~~~~~~~~

# Un appui sur une touche appelle cette fonction gérant l'interactivité
def Touche(event):
	# Si on presse Escape on quitte la fenêtre
	if (event.keysym=='Escape'):
		Mafenetre.destroy()

	# On n'effectue des actions de jeu qu'en dehors du mode pause	
	if (NouvellePartie.pause==0):
		
		# Les touches directionnelles font bouger le vaisseau dans les limites du cube	
		if	((event.keysym=='Up' and NouveauVaisseau.position[0]>0) or 
			(event.keysym=='Down' and NouveauVaisseau.position[0]<7) or\
			(event.keysym=='Left' and NouveauVaisseau.position[1]>0) or\
			(event.keysym=='Right' and NouveauVaisseau.position[1]<7)):
				NouveauVaisseau.move(event.keysym)

		# Touche de tir	
		if 	(event.keysym=='f'):
			NouveauVaisseau.fire()

		# Si un bonus est disponible, on l'active avec la touche "q"	
		if 	(event.keysym=='q' and NouveauVaisseau.bonus_available!=0):
			NouveauVaisseau.use_bonus()

		# Touche de cheat pour donner des bonus	
		if 	(event.keysym=='c'):
			NouveauVaisseau.bonus_available+=1	

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
    woosh = mixer.Sound("Sound/woosh.wav")
    laser = mixer.Sound("Sound/laser.wav") 
    laser_fat = mixer.Sound("Sound/laser_fat.wav")

except:
    print("Error: Sound file not found")

# ~~~~~~~~~~~~~~~~~~~ Fenêtre principale ~~~~~~~~~~~~~~~~~~~
	
Mafenetre = Tk()
Mafenetre.title('Space Defender')

# Un appui sur le clavier appelle la fonction Touche()
Mafenetre.bind('<Key>', Touche)

# Indication du joueur et du niveau en cours
PlayerLevel = Label(Mafenetre, text="Créer une nouvelle partie :", justify=LEFT) 
PlayerLevel.grid(padx=30, pady=5)

def NouvPart(event):
	woosh.play()
	global NouvellePartie
	NouvellePartie=Partie()
	global NouveauVaisseau
	NouveauVaisseau=Vaisseau()
BoutonNouvPart = Button(Mafenetre, text = "Nouvelle Partie")
BoutonNouvPart.bind("<Button-1>", NouvPart)
Mafenetre.bind("<Return>", NouvPart)
BoutonNouvPart.grid(padx=30, pady=5)


Mafenetre.mainloop()

