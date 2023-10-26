import os

from config import *


def remplissageImagesSonsJeu (url) -> list:
    vecteur = []
    for item in os.listdir(url):
        vecteur.append(os.path.join(url, item))
    return vecteur

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



