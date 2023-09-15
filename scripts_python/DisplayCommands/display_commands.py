"""
 ______  _____      _           _
|___   || ___ \    | |         | |
    / / | |_/ /___ | |__   ___ | |_
   / /  |    // _ \|  _ \ / _ \|  _|
  / /   | |\ \ (_) | |_) | (_) | |_
 /_/    |_| \_\___/|____/ \___/ \__|
                           7robot.fr

Cube8x8x8

Created by Robin Beilvert, Alexandre Proux
"""

from math import *  # noqa
import os
from pathlib import Path
from threading import Thread
from time import sleep


# Interface graphique
from tkinter import *

from led_cube import LedCube


ROOT_PATH = Path(__file__).parent
PATTERNS_PATH = ROOT_PATH / "Patterns"

# Nombre de nb_lignes
nb_lignes = 8
# Nombre de colonnes
nb_colonnes = 8
# Nombre d'étages
nb_etages = 8

# Etage affiché dans le canevas principal
Etage_courant = 0

# Taille d'un pixel des étages
etage_pix_size = 6

# Taille d'un pixel du canevas principal
pix_size = 50

# Variable logique d'envoi des trames (en cours ou pas)
envoiState = False
envoiFoncState = False


class Envoi_Trame(Thread):
    """Thread d'envoi de trame enregistrée"""

    def __init__(self, window):
        Thread.__init__(self)
        self._arret = False

        self.window = window
        self.led_cube = self.window.led_cube

        # Matrice tampon pour l'envoi de trames
        self.M = [
            [0] * nb_colonnes
            for _ in range(
                nb_lignes * nb_etages * (self.window.liste_trame.size() // 2)
            )
        ]

        for patt in range(self.window.liste_trame.size() // 2):
            filename = self.window.liste_trame.get(2 * patt)
            logs = open(PATTERNS_PATH / f"{filename}.txt", "r")
            for k in range(nb_etages):
                for i in range(nb_lignes):
                    for j in range(nb_colonnes):
                        for couleur_pixel in range(5):
                            # L'appel à logs.read(1) fait avancer la lecture d'un caractère :
                            # On se remet à la bonne position avec logs.seek()
                            logs.seek(8 * i + j + 64 * k, 0)
                            if logs.read(1) == "%s" % couleur_pixel:
                                self.M[i + 8 * k + 64 * patt][j] = couleur_pixel

    def run(self):
        numPattern = 0
        while not self._arret:
            for k in range(nb_etages):
                for i in range(nb_lignes):
                    for j in range(nb_colonnes):
                        self.led_cube.matrice_leds[i + 8 * k][j] = self.M[
                            i + 8 * k + 64 * numPattern
                        ][j]
            self.led_cube.Envoyer()

            # On attend le bon délai entre deux patterns
            delaistring = self.window.liste_trame.get(2 * numPattern + 1)
            sleep(int(delaistring[1 : len(delaistring) - 4]) / 1000.0)

            numPattern += 1
            if numPattern == self.window.liste_trame.size() // 2:
                numPattern = 0

            self.window.MAJ_Couleurs(False)
            self.window.MAJ_Couleurs(True)

        self.M = []
        print("Terminé !")

    def stop(self):
        self._arret = True


#####################################################################################################
################################ Thread d'envoi de trame de fonction ################################
#####################################################################################################
class Envoi_FoncTrame(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self._arret = False

        self.window = window
        self.led_cube = self.window.led_cube

    @staticmethod
    def get_field_value(field, t):  # noqa
        return max(0, min(7, int(eval(field.get()))))

    def run(self):
        t = 0
        while not self._arret:
            try:
                Xval = self.get_field_value(self.window.X_field, t)
            except Exception as e:
                print(e)
                Xval = 0
            try:
                Yval = 7 - self.get_field_value(self.window.Y_field, t)
            except Exception:
                Yval = 0
            try:
                Zval = 7 - self.get_field_value(self.window.Z_field, t)
            except Exception:
                Zval = 0

            self.led_cube.init_matrice_leds()

            for k in range(nb_etages):
                for i in range(nb_lignes):
                    for j in range(nb_colonnes):
                        if Yval == i and Xval == j and Zval == k:
                            self.led_cube.matrice_leds[i + 8 * k][j] = 3

            self.led_cube.Envoyer()

            t = t + 1

            self.window.MAJ_Couleurs(False)
            self.window.MAJ_Couleurs(True)

            # On attend le bon délai entre deux patterns
            if self.window.delai_field.get() != "":
                sleep(int(self.window.delai_field.get()) / 1000.0)
            else:
                sleep(0.1)

        print("Terminé !")

    def stop(self):
        self._arret = True


#####################################################################################################
#####################################################################################################


class MaFenetre(Tk):
    def __init__(self, led_cube):
        super().__init__()

        self.led_cube = led_cube

        # Les méthodes comme title, bind, etc. sont héritées de Tk
        self.title("Interface Cube8x8x8")

        # La méthode bind() permet de lier un événement avec une fonction :
        # un appui sur une touche du clavier provoquera l'appel de la fonction utilisateur Touche()
        self.bind("<Key>", self.Touche)

        self.bind("<Left>", self.ChangeEtage)
        self.bind("<Right>", self.ChangeEtage)

        Boutons = Canvas(self, width=100, height=100)

        #####################################################################################################
        ##~~~~~~~~~~~~~~~~~~~~~~ Création de la ligne avec les étages et les flèches ~~~~~~~~~~~~~~~~~~~~~~##
        #####################################################################################################
        self.etages = Canvas(self, width=8 * 51, height=50)

        self.Fleche_gauche = Canvas(self, width=48, height=48)
        self.Fleche_gauche.grid(row=0, column=0)
        photo_flechegauche = PhotoImage(file=ROOT_PATH / "fleche_gauche.png")
        self.Fleche_gauche.create_image(0, 0, image=photo_flechegauche, anchor=NW)

        self.Fleche_droite = Canvas(self, width=48, height=48)
        self.Fleche_droite.grid(row=0, column=6)
        photo_flechedroite = PhotoImage(file=ROOT_PATH / "fleche_droite.png")
        self.Fleche_droite.create_image(0, 0, image=photo_flechedroite, anchor=NW)

        self.etages.grid(row=0, column=1, columnspan=5, pady=5)

        # On lie les flèches du clavier aux flèches de sélection des étages
        self.Fleche_gauche.bind("<Button-1>", self.ChangeEtage)
        self.Fleche_droite.bind("<Button-1>", self.ChangeEtage)
        #####################################################################################################

        #####################################################################################################
        ##~~~~~~~~~~~~~~~~~~~~~~~ Création du canevas principal (matrice colorée) ~~~~~~~~~~~~~~~~~~~~~~~~~##
        #####################################################################################################
        Hauteur = nb_lignes * pix_size
        Largeur = nb_colonnes * pix_size
        self.Canevas = Canvas(self, width=Largeur + 2, height=Hauteur + 2)

        # La méthode bind() permet de lier un événement avec une fonction :
        # un clic gauche sur la zone graphique provoquera l'appel de la fonction utilisateur Clic()
        self.Canevas.bind("<Button-1>", self.Clic)
        # On affiche le canevas principal
        self.Canevas.grid(row=1, column=1, columnspan=5)
        #####################################################################################################

        #####################################################################################################
        ##~~~~ Boutons de sélection de la zone concernée par les entrées au clavier et image du clavier ~~~##
        #####################################################################################################
        Boutons = Canvas(self, width=100, height=100, highlightthickness=0)

        ImgClavier = Canvas(Boutons, width=329, height=146)
        ImgClavier.grid(column=0, rowspan=2)
        photo = PhotoImage(file=ROOT_PATH / "clavier.png")
        ImgClavier.create_image(0, 0, image=photo, anchor=NW)

        self.section = IntVar()
        self.section.set(0)
        bouton1 = Radiobutton(
            Boutons,
            text="En haut",
            variable=self.section,
            value=0,
            indicatoron=False,
            height=4,
            width=11,
        )
        bouton2 = Radiobutton(
            Boutons,
            text="En bas",
            variable=self.section,
            value=1,
            indicatoron=False,
            height=4,
            width=11,
        )
        bouton1.grid(row=0, column=1)
        bouton2.grid(row=1, column=1)

        Boutons.grid(row=2, column=1, columnspan=5, pady=5)
        #####################################################################################################

        #####################################################################################################
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Gestion des trames de patterns ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
        #####################################################################################################
        Gestion_Trames = Canvas(self, highlightthickness=0)
        Gestion_Trames.grid(row=0, column=7, rowspan=3, padx=10)

        Button(
            Gestion_Trames,
            text="Supprimer pattern \n /!\\ Suppression définitive /!\\",
            fg="red",
            width=21,
            command=self.Supprimer_Pattern,
        ).grid(row=0, column=0, columnspan=2, pady=5)
        Label(Gestion_Trames, text="Patterns disponibles :").grid(
            row=1, column=0, columnspan=2
        )
        self.liste_save = Listbox(Gestion_Trames, width=24, height=5)
        self.liste_save.grid(row=2, column=0, columnspan=2, rowspan=2)
        self.Actualiser_patterns()

        Fleche_haut = Canvas(Gestion_Trames, width=24, height=24)
        Fleche_haut.grid(row=2, column=2)
        photo_flechehaut = PhotoImage(file=ROOT_PATH / "fleche_haut.png")
        Fleche_haut.create_image(0, 0, image=photo_flechehaut, anchor=NW)

        Fleche_bas = Canvas(Gestion_Trames, width=24, height=24)
        Fleche_bas.grid(row=3, column=2)
        photo_flechebas = PhotoImage(file=ROOT_PATH / "fleche_bas.png")
        Fleche_bas.create_image(0, 0, image=photo_flechebas, anchor=NW)

        Label(Gestion_Trames, text="Trame envoyée").grid(row=4, column=0, columnspan=3)
        self.liste_trame = Listbox(Gestion_Trames, width=24, height=15)
        self.liste_trame.grid(row=5, column=0, columnspan=2)

        Button(
            Gestion_Trames, text="Ajouter", command=self.Ajouter_Pattern, width=8
        ).grid(row=6, column=0, pady=6)
        Button(
            Gestion_Trames, text="Enlever", command=self.Enlever_Pattern, width=8
        ).grid(row=6, column=1, pady=6)

        Button(Gestion_Trames, text="Délai :", command=self.Modif_Delai, width=8).grid(
            row=7, column=0, pady=5
        )
        self.delai_field = Entry(Gestion_Trames, width=9)
        self.delai_field.grid(row=7, column=1)
        Label(Gestion_Trames, text="(Par défaut : 100ms)").grid(
            row=8, column=0, columnspan=2
        )
        #####################################################################################################

        #####################################################################################################
        ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Gestion de fonctions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
        #####################################################################################################
        Gestion_Fonctions = Canvas(self, highlightthickness=0)
        Gestion_Fonctions.grid(row=1, column=8, padx=10)

        Label(Gestion_Fonctions, text="Coordonées souhaitées").grid(
            row=0, column=0, columnspan=2
        )

        Label(Gestion_Fonctions, text="X(t) =").grid(row=1)
        self.X_field = Entry(Gestion_Fonctions, width=9)
        self.X_field.grid(row=1, column=1, pady=5)

        Label(Gestion_Fonctions, text="Y(t) =").grid(row=2)
        self.Y_field = Entry(Gestion_Fonctions, width=9)
        self.Y_field.grid(row=2, column=1, pady=5)

        Label(Gestion_Fonctions, text="Z(t) =").grid(row=3)
        self.Z_field = Entry(Gestion_Fonctions, width=9)
        self.Z_field.grid(row=3, column=1, pady=5)
        #####################################################################################################

        #####################################################################################################
        #####################################################################################################
        Boutons_Envoi = Canvas(Gestion_Fonctions, highlightthickness=0)
        Boutons_Envoi.grid(row=4, columnspan=2, pady=40)

        self.trameselect = IntVar()
        self.trameselect.set(0)
        Radiobutton(
            Boutons_Envoi,
            text="Trame\nenregistrée",
            variable=self.trameselect,
            value=0,
            indicatoron=False,
            height=2,
            width=10,
        ).grid(row=0)
        Radiobutton(
            Boutons_Envoi,
            text="Fonction 3D",
            variable=self.trameselect,
            value=1,
            indicatoron=False,
            height=2,
            width=10,
        ).grid(row=0, column=1)

        self.Bouton_EnvoiTrames = Button(
            Boutons_Envoi,
            text="Envoyer\nla trame !",
            command=self.Envoyer_Trame,
            height=4,
            width=19,
            fg="purple",
            cursor="hand1",
        )
        self.Bouton_EnvoiTrames.grid(row=1, columnspan=2, pady=10)
        #####################################################################################################

        # On remplit le canevas principal et les étages de carrés blancs
        self.Init()

        # Bouton Envoyer
        Button(self, text="Envoyer", fg="purple", command=self.led_cube.Envoyer).grid(
            row=3, column=1, pady=5
        )

        # Bouton Effacer
        Button(self, text="Effacer", command=self.Init).grid(row=3, column=2, pady=5)

        # Bouton Open
        Button(self, text="Open", command=self.Open).grid(row=3, column=3, pady=5)

        # Bouton Save
        Button(self, text="Save", command=self.Save_Popup).grid(row=3, column=4, pady=5)

        # Bouton Quitter
        Button(self, text="Quitter", command=self.destroy).grid(row=3, column=5, pady=5)

        self.mainloop()

    #####################################################################################################
    #####################################################################################################

    def Envoyer_Trame(self):
        global envoiState
        global envoiFoncState
        # Envoi d'une trame enregistrée
        if self.trameselect.get() == 0:
            # Si une trame de fonction est en cours d'envoi, on l'arrête :
            if envoiFoncState:
                global envoiFoncTrame
                self.Bouton_EnvoiTrames.config(text="Envoyer\nla trame !", fg="purple")
                envoiFoncTrame.stop()  # On arrête l'envoi
                envoiFoncState = not envoiState
            # Si la liste de patterns n'est pas vide, on envoie ce qu'elle contient :
            if self.liste_trame.size() != 0:
                # Si un envoi est déjà en cours, on l'arrête :
                if envoiState:
                    global envoiTrame
                    self.Bouton_EnvoiTrames.config(
                        text="Envoyer\nla trame !", fg="purple"
                    )
                    envoiTrame.stop()  # On arrête l'envoi
                # Si aucun envoi n'est en cours, on envoie la trame :
                else:
                    self.Bouton_EnvoiTrames.config(text="Arrêter\nl'envoi", fg="brown")
                    envoiTrame = Envoi_Trame(self)
                    envoiTrame.start()  # On démarre l'envoi
                # Inversion de l'état d'envoi
                envoiState = not envoiState
            else:
                print("Trame vide...")

        # Envoi d'une trame de fonction
        else:
            # Si une trame enregistrée est en cours d'envoi, on l'arrête :
            if envoiState:
                # global envoiTrame
                self.Bouton_EnvoiTrames.config(text="Envoyer\nla trame !", fg="purple")
                envoiTrame.stop()  # On arrête l'envoi
                envoiState = not envoiState
            # Si un envoi est déjà en cours, on l'arrête :
            if envoiFoncState:
                # global envoiFoncTrame
                self.Bouton_EnvoiTrames.config(text="Envoyer\nla trame !", fg="purple")
                envoiFoncTrame.stop()  # On arrête l'envoi
            # Si aucun envoi n'est en cours, on envoie la trame :
            else:
                self.Bouton_EnvoiTrames.config(text="Arrêter\nl'envoi", fg="brown")
                envoiFoncTrame = Envoi_FoncTrame(self)
                envoiFoncTrame.start()  # On démarre l'envoi
            # Inversion de l'état d'envoi
            envoiFoncState = not envoiFoncState

    def Change_couleur(self, i, j):
        # Incrémentation de la matrice
        self.led_cube.matrice_leds[i + 8 * Etage_courant][j] = (
            self.led_cube.matrice_leds[i + 8 * Etage_courant][j] + 1
        ) % 4

        # Changement de couleur des carrés
        if self.led_cube.matrice_leds[i + 8 * Etage_courant][j] == 1:
            self.Canevas.itemconfigure(carre[i][j], fill="red")
            self.etages.itemconfigure(
                carres_etages[i + 8 * Etage_courant][j], fill="red"
            )

        elif self.led_cube.matrice_leds[i + 8 * Etage_courant][j] == 2:
            self.Canevas.itemconfigure(carre[i][j], fill="blue")
            self.etages.itemconfigure(
                carres_etages[i + 8 * Etage_courant][j], fill="blue"
            )

        elif self.led_cube.matrice_leds[i + 8 * Etage_courant][j] == 3:
            self.Canevas.itemconfigure(carre[i][j], fill="purple")
            self.etages.itemconfigure(
                carres_etages[i + 8 * Etage_courant][j], fill="purple"
            )

        else:
            self.Canevas.itemconfigure(carre[i][j], fill="white")
            self.etages.itemconfigure(
                carres_etages[i + 8 * Etage_courant][j], fill="white"
            )

    def Clic(self, event):
        """Gestion de l'événement Clic gauche sur la zone graphique"""
        for i in range(nb_lignes):
            for j in range(nb_colonnes):
                if (j * pix_size < event.x <= (j + 1) * pix_size) and (
                    i * pix_size < event.y <= (i + 1) * pix_size
                ):
                    self.Change_couleur(i, j)

    def Touche(self, event):
        # Gestion de l'événement Appui sur une touche du clavier
        touche = event.keysym

        if touche == "Escape":
            self.destroy()

        if touche == "asterisk":
            self.Init()

        if touche == "parenright":
            self.Open()

        if touche == "equal":
            self.Save_Popup()

        if touche == "Return":
            self.led_cube.Envoyer()

        if touche == "Up":
            self.section.set(0)
        if touche == "Down":
            self.section.set(1)

        # Touches sensibles pour les pixels
        sensPix_list = [
            "ampersand",
            "eacute",
            "quotedbl",
            "apostrophe",
            "parenleft",
            "minus",
            "egrave",
            "underscore",
            "a",
            "z",
            "e",
            "r",
            "t",
            "y",
            "u",
            "i",
            "q",
            "s",
            "d",
            "f",
            "g",
            "h",
            "j",
            "k",
            "w",
            "x",
            "c",
            "v",
            "b",
            "n",
            "comma",
            "semicolon",
        ]
        # Touches sensibles changement d'étage
        sensEtage_list = ["Left", "Right"]

        for index in range(len(sensPix_list)):
            if touche == sensPix_list[index]:
                self.Change_couleur(index // 8 + 4 * self.section.get(), index % 8)

        for index in range(len(sensEtage_list)):
            if touche == sensEtage_list[index]:
                self.ChangeEtage(index)

    def Init(self):
        """Initialisation des étages"""

        # Contours des étages
        self.etages.delete(ALL)
        global etage
        etage = []
        for i in range(nb_etages):
            etage = etage + [
                self.etages.create_rectangle(
                    48 * i + 3 * (i + 1),
                    2,
                    48 * (i + 1) + 3 * (i + 1),
                    50,
                    width=2,
                    outline="grey",
                )
            ]
        self.etages.itemconfigure(etage[Etage_courant], outline="yellow")

        # Contenu des étages
        global carres_etages
        carres_etages = []
        # Initialisation des carrés étage par étage et ligne par ligne
        for i in range(nb_lignes * nb_etages):
            # On créé une ligne
            sommelist = []
            for j in range(8):
                sommelist = sommelist + [
                    self.etages.create_rectangle(
                        j * etage_pix_size + 3 + 51 * (i // 8),
                        (i % 8) * etage_pix_size + 2,
                        j * etage_pix_size + etage_pix_size + 2 + 51 * (i // 8),
                        (i % 8) * etage_pix_size + etage_pix_size + 1,
                        outline="white",
                        fill="white",
                    )
                ]
            # On ajoute la ligne
            carres_etages.append(sommelist)

        #####################################################################################################

        ################################ Initialisation du canevas principal ################################

        self.Canevas.delete(ALL)
        global carre
        carre = []
        # Initialisation des carrés ligne par ligne
        for i in range(nb_lignes):
            # On créé une ligne
            sommelist = []
            for j in range(8):
                sommelist = sommelist + [
                    self.Canevas.create_rectangle(
                        j * pix_size + 2,
                        i * pix_size + 2,
                        j * pix_size + pix_size + 1,
                        i * pix_size + pix_size + 1,
                        outline="white",
                        fill="white",
                    )
                ]
            # On ajoute la ligne
            carre.append(sommelist)

        # RAZ de la matrice
        for k in range(nb_etages):
            for i in range(nb_lignes):
                for j in range(nb_colonnes):
                    self.led_cube.matrice_leds[i + 8 * k][j] = 0

    ####################################################################################################

    def ChangeEtage(self, event):
        global Etage_courant
        # Touche est pour un évenement au clavier, event.widget gère les interventions à la souris
        touche = event.keysym

        self.etages.itemconfigure(etage[Etage_courant], outline="grey")

        if touche == "Left" or event.widget == self.Fleche_gauche:
            if Etage_courant != 0:
                Etage_courant = Etage_courant - 1
        else:
            if Etage_courant != 7:
                Etage_courant = Etage_courant + 1

        self.etages.itemconfigure(etage[Etage_courant], outline="yellow")

        self.MAJ_Couleurs(False)

    def MAJ_Couleurs(self, petits_carres):
        if petits_carres:
            for k in range(nb_etages):
                for i in range(nb_lignes):
                    for j in range(nb_colonnes):
                        if self.led_cube.matrice_leds[i + 8 * k][j] == 1:
                            self.etages.itemconfigure(
                                carres_etages[i + 8 * k][j], fill="red"
                            )
                        elif self.led_cube.matrice_leds[i + 8 * k][j] == 2:
                            self.etages.itemconfigure(
                                carres_etages[i + 8 * k][j], fill="blue"
                            )
                        elif self.led_cube.matrice_leds[i + 8 * k][j] == 3:
                            self.etages.itemconfigure(
                                carres_etages[i + 8 * k][j], fill="purple"
                            )
                        else:
                            self.etages.itemconfigure(
                                carres_etages[i + 8 * k][j], fill="white"
                            )
        else:
            for i in range(nb_lignes):
                for j in range(nb_colonnes):
                    if self.led_cube.matrice_leds[i + 8 * Etage_courant][j] == 1:
                        self.Canevas.itemconfigure(carre[i][j], fill="red")
                    elif self.led_cube.matrice_leds[i + 8 * Etage_courant][j] == 2:
                        self.Canevas.itemconfigure(carre[i][j], fill="blue")
                    elif self.led_cube.matrice_leds[i + 8 * Etage_courant][j] == 3:
                        self.Canevas.itemconfigure(carre[i][j], fill="purple")
                    else:
                        self.Canevas.itemconfigure(carre[i][j], fill="white")

    def Open(self):
        if self.liste_save.curselection() != ():
            filename = self.liste_save.get(self.liste_save.curselection())
            logs = open(PATTERNS_PATH / f"{filename}.txt", "r")
            for k in range(nb_etages):
                for i in range(nb_lignes):
                    for j in range(nb_colonnes):
                        for couleur_pixel in range(5):
                            # L'appel à logs.read(1) fait avancer la lecture d'un caractère :
                            # On se remet à la bonne position avec logs.seek()
                            logs.seek(8 * i + j + 64 * k, 0)
                            if logs.read(1) == "%s" % couleur_pixel:
                                self.led_cube.matrice_leds[i + 8 * k][j] = couleur_pixel

            logs.close()
            self.MAJ_Couleurs(False)
            self.MAJ_Couleurs(True)

    def Actualiser_patterns(self):
        # Actualisation de la liste des patterns enregistrés
        self.liste_save.delete(0, END)
        savedPatterns = (ROOT_PATH / "Patterns").iterdir()
        for pattern in savedPatterns:
            self.liste_save.insert(END, pattern.stem)

    def Save_Popup(self):
        def Save(event):
            if savefield.get() == "":
                # Nom de sauvegarde par défaut
                savename = "default"
            else:
                savename = savefield.get()

            logs = open(PATTERNS_PATH / f"{savename}.txt", "w")
            for k in range(nb_etages):
                for i in range(nb_lignes):
                    for j in range(nb_colonnes):
                        logs.write("%s" % self.led_cube.matrice_leds[i + 8 * k][j])
            logs.close()

            self.Actualiser_patterns()

            Save_Screen.destroy()

        # Création de la fenêtre de sauvegarde
        Save_Screen = Tk()
        Save_Screen.title("Save")

        Label(Save_Screen, text="Nom du pattern (default par defaut):").grid()

        global savefield
        savefield = Entry(Save_Screen)
        savefield.focus_force()
        savefield.grid()

        # Bouton Save
        saveBouton = Button(Save_Screen, text="Save")
        saveBouton.bind("<Button-1>", Save)
        Save_Screen.bind("<Return>", Save)
        saveBouton.grid()

    def Supprimer_Pattern(self):
        print("%s" % self.delai_field.get())
        os.remove(
            PATTERNS_PATH / f"{self.liste_save.get(self.liste_save.curselection())}.txt"
        )
        self.Actualiser_patterns()

    def Ajouter_Pattern(self):
        if self.liste_save.curselection() != ():
            self.liste_trame.insert(
                END, self.liste_save.get(self.liste_save.curselection())
            )

            if self.delai_field.get() == "":
                self.liste_trame.insert(END, "(100 ms)")
            else:
                self.liste_trame.insert(END, "(%s ms)" % self.delai_field.get())

    def Enlever_Pattern(self):
        if self.liste_trame.curselection() != ():
            n = self.liste_trame.curselection()[0]
            self.liste_trame.delete(2 * (n // 2), 2 * (n // 2) + 1)

    def Modif_Delai(self):
        if self.liste_trame.curselection() != ():
            n = self.liste_trame.curselection()[0]
            self.liste_trame.delete(2 * (n // 2) + 1)
            self.liste_trame.insert(
                2 * (n // 2) + 1, "(%s ms)" % self.delai_field.get()
            )


#####################################################################################################
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
#####################################################################################################


def run():
    led_cube = LedCube(nb_lignes, nb_colonnes, nb_etages)

    # Création de la fenêtre principale
    MaFenetre(led_cube)


if __name__ == "__main__":
    run()
