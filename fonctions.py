import os
from config import *


def recupererdialogue(url) -> list:
    dialogues = []
    with open(url, "r") as file:
        dialogues = file.read().split(";")
    return dialogues


def remplissageImagesSonsJeu(url) -> list:
    vecteur = []
    for item in os.listdir(url):
        vecteur.append(os.path.join(url, item))
    return vecteur


def calculListePositionObjets(nb, taille) -> list:
    vec = []
    for i in range(0, nb):
        position = (100 + taille * 2 * i, 300)
        vec.append(position)
    return vec

def calculListePositionBriquesL2(nb, taille, fenetrelargeur, fenetrehauteur) -> list:
    vec = []
    for i in range (0 , nb):
        position = (fenetrelargeur - taille*2, fenetrehauteur - (i * 300))
        vec.append(position)
    return vec

def remplissageVecteur(fichiers):
    vecteur = []
    for fichier in fichiers:
        vecteur.append(fichier)
    return vecteur


def affichageDecor(fenetre, decorx, itemdecor, fenetrelargeur, fenetrehauteur):

    fenetre.blit(itemdecor, (decorx, fenetrehauteur - 6 - itemdecor.get_height()))


def affichageDecorL2(fenetre, decorx, itemdecor, fenetrelargeur, fenetrehauteur, decory, offset):
    fenetre.blit(itemdecor, (decorx, decory+offset))
