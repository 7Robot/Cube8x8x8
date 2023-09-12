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

import sys
import os						# Sauver des fichiers (scores)
from math import *				# Utilisation de fonctions mathématiques
from serial import * 
from collections import deque 	# Opérations avancés sur les listes (rotate)
from random import randint    	# Entiers aléatoires
from time import sleep			# Pauses dans le programme
from pygame import mixer      	# Jouer des sons
from threading import Thread 	# Gestionnaire de threads

# Bibliothèque pour interface graphique
try:
	# for Python2
	from Tkinter import *
except ImportError:
	# for Python3
	from tkinter import *

# Dimension du cube
dimension = 8

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~ Classes ~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Partie:

	def __init__(self):
		music.stop()		
		try:
			self.difficulty=NouvellePartie.difficulty
		except Exception:
			self.difficulty=0
		# Délai d'actualisation : 480-40*difficulty
		self.nom_joueur="Anonyme"
		self.Nom_Joueur()
		self.pause=1
		self.perdu=0
		self.niveau=0
		self.liste_attaquants=[]

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
		self.liste_tirs=[]

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
			self.liste_tirs.append(LaserFat())
			laser_fat.play()
			# On enlève un tir bonus
			self.bonus_count-=1	
		# Si on n'a pas de tir bonus en stock	
		else:
			self.liste_tirs.append(Laser())
			laser.play()

	# Cette fonction est appellée par la touche "q" si des bonus sont disponibles
	def use_bonus(self):
		# On ajoute 10 tirs bonus disponibles
		self.bonus_count+=10
		# On décrémente le nombre de bonus disponibles
		self.bonus_available-=1

class Attaquant():
	def __init__(self):
		global dimension
		# Position initiale aléatoire de l'attaquant dans le dernier plan du cube ([etage, ligne, colonne])
		self.position=[randint(0, dimension-1),0,randint(0, dimension-1)]
		self.vitesse=randint(45, 55)-4*NouvellePartie.difficulty
	def move(self,i):
		if i%int(self.vitesse/10)==0:
			self.position[1]+=1	
	def __del__(self):
		shot.play()

class Tir():
	def __init__(self):
		self.position=[0,7,0]
		self.position[0]=NouveauVaisseau.position[0]
		self.position[2]=NouveauVaisseau.position[1]
		self.vitesse=50-4*9
	def move(self,i):
		if i%int(self.vitesse/10)==0:
			self.position[1]-=1

class Laser(Tir):
	def __init__(self):
		Tir.__init__(self)
		super(Laser, self).__init__()


class LaserFat(Tir):
	def __init__(self):
		#Tir.__init__(self)
		super(LaserFat, self).__init__()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~ Thread parallèle de partie en cours ~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def PartieEnCours():
	i=0
	while True:
		while NouvellePartie.pause==0:
			l=0
			# On fait avancer les attaquants
			while l < len(NouvellePartie.liste_attaquants):
				if NouvellePartie.liste_attaquants[l].position[1]<7:
					NouvellePartie.liste_attaquants[l].move(i)
					l+=1
				else:
					del NouvellePartie.liste_attaquants[l]
			l=0		
			# On fait avancer les tirs
			while l < len(NouveauVaisseau.liste_tirs):
				if NouveauVaisseau.liste_tirs[l].position[1]>0:
					NouveauVaisseau.liste_tirs[l].move(i)
					l+=1
				else:
					del NouveauVaisseau.liste_tirs[l]
			# On actualise et envoie l'image 3D du cube
			Envoyer()
			i+=1
			sleep(0.2)
		sleep(0.1)		

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~ Fonctions ~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

		#CHEAT#CHEAT#CHEAT#CHEAT#CHEAT#CHEAT#CHEAT#CHEAT#CHEAT#
		# Touche de cheat pour donner des bonus	
		if 	(event.keysym=='c'):
			NouveauVaisseau.bonus_available+=1	

		if 	(event.keysym=='a'):
			NouvellePartie.liste_attaquants.append(Attaquant())
			print(len(NouvellePartie.liste_attaquants))
			print(NouveauVaisseau.position)

		if 	(event.keysym=='t'):
			NouvellePartie.liste_attaquants.append(Attaquant())
		#CHEAT#CHEAT#CHEAT#CHEAT#CHEAT#CHEAT#CHEAT#CHEAT#CHEAT#	

	# Si on presse espace et qu'on n'a pas perdu on se met en pause ou on en sort
	if (event.keysym=='space' and NouvellePartie.perdu == 0):
		if (NouvellePartie.pause == 1):
			NouvellePartie.pause = 0
			music.play(-1)
		else:
			NouvellePartie.pause = 1
			music.stop()


# Fonction d'envoi de la matrice au ftdi
# Nécessite matrice_leds
def Envoyer():
	global dimension
	# Matrice pour envoyer les infos de l'interface graphique au ftdi
	M = []
	for i in range(dimension*dimension):
		M.append([0] * dimension)

	# Etages
	for k in range(dimension):	
		# Lignes
		for i in range(dimension) :
			# Colonnes
			for j in range(dimension) :	
				# Détection du vaisseau (toujours sur la 7eme ligne)
				if i==7 and NouveauVaisseau.position==[k, j]:
					M[i+dimension*k][j]=3
				# Détection des attaquants
				for l in range(len(NouvellePartie.liste_attaquants)):
					if NouvellePartie.liste_attaquants[l].position==[k, i, j]:	
						M[i+dimension*k][j]=2
				# Détection des tirs
				for l in range(len(NouveauVaisseau.liste_tirs)):
					if NouveauVaisseau.liste_tirs[l].position==[k, i, j]:	
						M[i+dimension*k][j]=1

	octets_rouges=[]				
	octets_bleus=[]
	for k in range(dimension):
		octets_rouges.append([0] * dimension)
		octets_bleus.append([0] * dimension)		

	for k in range(dimension):	
		# Indice pour chaque PIC
		for i in range(dimension) :
			# Indice pour chaque diode d'une ligne (= d'un PIC)
			for j in range(dimension) :
				
				if i%2==0 and (j//4)%2==1:
					l=1
					c=-4
				elif i%2==1 and (j//4)%2==0:
					l=-1
					c=4
				else:
					l=0
					c=0

				if  M[i+l+8*k][j+c] == 1:
					octets_rouges[k][i] = octets_rouges[k][i]+2**j

				elif M[i+l+8*k][j+c] == 2:                
					octets_bleus[k][i] = octets_bleus[k][i]+2**j

				elif M[i+l+8*k][j+c] == 3:
					octets_rouges[k][i] = octets_rouges[k][i]+2**j
					octets_bleus[k][i] = octets_bleus[k][i]+2**j

	######## Avec l'ancienne librairie pylibftdi ########
	try:
		# On envoie la sauce !
		with Device (mode = 't') as dev:
			dev.baudrate = 115200

			# 8 étages
			for k in range(dimension) :
				# 8 PICs = 8 lignes bicolores
				for i in range (dimension) :
					dev.write(chr(octets_bleus[k][i]))
					dev.write(chr(octets_rouges[k][i]))
	except Exception:	
		print('FTDI non détecté')

	"""
	######## Avec la nouvelle librairie pyserial ########
	try:
		# On envoie la sauce !
		dev = Serial('/dev/ttyUSB0', 115200)
		# 8 étages
		for k in range(dimension) :
			# 8 PICs = 8 lignes bicolores
			for i in range (dimension) :
				dev.write(chr(octets_bleus[k][i]).encode())
				dev.write(chr(octets_rouges[k][i]).encode())
	except Exception:	
		print('FTDI non détecté')
	"""
	

# Ce qui est sous le if est executé que si on lance directement le script
# mais pas dans le cas d'un import :
if __name__ == '__main__':

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# ~~~~~~~~~~~~~~~~~~~ Gestion de l'audio ~~~~~~~~~~~~~~~~~~~
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	# Initialize the pygame mixer
	mixer.init(44100)
	try:
		# Create the sound instances
		music = mixer.Sound("Sound/E1M1.wav")
		woosh = mixer.Sound("Sound/woosh.wav")
		laser = mixer.Sound("Sound/laser.wav") 
		laser_fat = mixer.Sound("Sound/laser_fat.wav")
		shot = mixer.Sound("Sound/shot.wav")

	except:
		print("Error: Sound file not found")

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# ~~~~~~~~~~~~~~~~~~~ Fenêtre principale ~~~~~~~~~~~~~~~~~~~
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

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
		Thread(None, PartieEnCours).start()

	BoutonNouvPart = Button(Mafenetre, text = "Nouvelle Partie")
	BoutonNouvPart.bind("<Button-1>", NouvPart)
	Mafenetre.bind("<Return>", NouvPart)
	BoutonNouvPart.grid(padx=30, pady=5)

	Mafenetre.mainloop() 
	NouvellePartie.pause=1
	Thread(None, PartieEnCours)._stop() 
	music.stop()  

