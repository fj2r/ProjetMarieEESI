import os

from config import *

def recupererdialogue (url) -> list:
    dialogues = []
    with open(url,"r") as file:
        dialogues = file.read().split(";")
    return dialogues

def remplissageImagesSonsJeu (url) -> list:
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
def remplissageVecteur(fichiers):
    vecteur = []
    for fichier in fichiers:
        vecteur.append(fichier)
    return vecteur


def affichageDecor(fenetre, decorx, itemdecor, fenetrelargeur, fenetrehauteur):
    # positionnement des éléments de décor
    """fenetre.blit(
        itemdecor,
        (
            decorx - itemdecor.get_width(),
            fenetrehauteur - 6 - itemdecor.get_height(),
        ),
    )"""
    fenetre.blit(itemdecor, (decorx, fenetrehauteur - 6 - itemdecor.get_height()))
    """fenetre.blit(
        itemdecor,
        (
            decorx + itemdecor.get_width(),
            fenetrehauteur - 6 - itemdecor.get_height(),
        ),
    )"""



