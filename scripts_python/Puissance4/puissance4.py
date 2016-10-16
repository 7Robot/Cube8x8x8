#!/usr/bin/env python 
# -*- coding: utf8 -*-

#initialise la matrice
def initMatrice(dimension):
    matrice = []
    for i in range(dimension):
        l_temp = []
        for j in range(dimension):
            l_temp.append([0] * dimension) #Ajoute 10 colonnes de 10 entiers(int) ayant pour valeurs 0
        matrice.append(l_temp)
    return matrice

#met la valeur de la case [ligne,colonne,etage] de matrice a val
def setCellule(matrice,ligne,colonne,etage,val):
    matrice[etage][colonne][ligne] = val

#recupere la valeur de la case [ligne,colonne,etage] de matrice
def getCellule(matrice,ligne,colonne,etage):
    return matrice[etage][colonne][ligne]

#fonction qui permet au joueur de mettre une piece retourne l etage
def choisirCase(matrice,dimension,ligne,colonne,joueur):
    fini = False
    etage = 0
    while (not fini) and (etage<dimension):
        if getCellule(matrice,ligne,colonne,etage) == 0:
            setCellule(matrice,ligne,colonne,etage,joueur)
            fini = True
        else:
            etage = etage +1    
    return etage

#fonction qui retourne le prochain joueur qui doit joueur
def changerJoueur(joueur):
    if joueur == 1:
       return 2
    else:
        return 1

#fonction qui permet au joueur de choisir une case
def choixCase ():
    ligne = input("ligne : ")
    colonne = input("colonne :")
    return [ligne,colonne]

def verifRec(matrice,newLigne,newCol,newEtage,oldLigne,oldCol,oldEtage,val,etape):
    if getCellule(matrice,newLigne,newCol,newEtage) != val:
       return False
    elif (getCellule(matrice,newLigne,newCol,newEtage) == val) and etape == 4:
       return True
    else
        nLigne = 2*newLigne - oldLigne
        nCol = 2*newCol - oldCol
        nEtage = 2*newEtage - oldEtage
        return verifRec(matrice,nLigne,nCol,nEtage,newLigne,newCol,newEtage,val,etape+1)

def 
def verif(matrice,dimension,ligne,col,etage):
    puissance = False
    val = getCellule(ligne,col,etage)
    #teste l interieur du cube
    if ligne>0 and ligne<dimension-1 and col>0 and col<dimension-1 and etage>0 and etage<dimension-1:
        #parcours les cases autour de la case courante pour voir si on a le puissance4 
        e=etage-1
        while e<=etage+1
            c=col-1
            while c<=col+1
                l=ligne-1
                while l<=ligne+1
                    if e!=etage or c!=col or l!=ligne
                        puissance = puissance or verifRec(matrice,l,c,e,ligne,col,etage,val,2) 
                    l+1
                c+1
            e+1
    #
    elif 
    return puissance

def jouer(m):
    dimension = m
    matrice = initMatrice(dimension)
    print matrice
    joueur = 1
    gagner = False
    while not gagner:
        licol = choixCase()
        ligne = licol[0]
        colonne = licol[1]
        etage = choisirCase(matrice,dimension,ligne,colonne,joueur)
        while etage ==dimension:
            licol = choixCase()
            ligne = licol[0]
            colonne = licol[1]
            etage = choisirCase(matrice,dimension,ligne,colonne,joueur)
        print matrice
        #joueur = changerJoueur(joueur)
        #print joueur

jouer(4)
       
    
    


