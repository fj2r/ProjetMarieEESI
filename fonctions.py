import os

from conf import *


def remplissageImagesSonsJeu (url):
    vecteur = []
    for item in os.listdir(url):
        vecteur.append(os.path.join(url, item))
    return vecteur

def remplissageVecteur(fichiers):
    vecteur = []
    for fichier in fichiers:
        vecteur.append(fichier)
    return vecteur


def affichageDecor(fenetre, decorx, herbederriere, fenetrelargeur, fenetrehauteur):
    # en fond de décor
    if decorx <= -fenetrelargeur or decorx >= fenetrelargeur:
        decorx = 0

    fenetre.blit(
        herbederriere,
        (
            decorx - herbederriere.get_width(),
            fenetrehauteur - 6 - herbederriere.get_height(),
        ),
    )
    fenetre.blit(
        herbederriere, (decorx, fenetrehauteur - 6 - herbederriere.get_height())
    )
    fenetre.blit(
        herbederriere,
        (
            decorx + herbederriere.get_width(),
            fenetrehauteur - 6 - herbederriere.get_height(),
        ),
    )


fichierssons = remplissageImagesSonsJeu("son/sfx/ogg/")