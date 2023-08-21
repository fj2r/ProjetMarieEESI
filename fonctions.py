from conf import *


def remplissageVecteur(fichiers):
    vecteur = []
    for fichier in fichiers:
        vecteur.append(fichier)
    return vecteur


def affichageDecor(fenetre, decorx, herbederriere):
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

    ''''#fenetre.blit(
        sol, (decorx - 6, fenetrehauteur - 6 - 10)
    )
    #fenetre.blit(sol, (decorx, fenetrehauteur - sol.get_height() - 10))
    #fenetre.blit(
        sol, (decorx + 6 , fenetrehauteur - 6) - 10)
    )'''
