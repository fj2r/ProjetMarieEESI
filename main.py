#################################################################
#
#       Jeu en Pygame pour projet EESI
#       Graphics by Marie
#       Coding by Fred - python 3.8
#       ver. alpha-0.1
#
#################################################################
import sys

from classes import *
from conf import *
from fonctions import *


def main():
    pg.init()  # initialisation des modules
    pg.mixer.init()

    jeu = jeuetatinitial

    #########################################
    # définition de la fenetre principale du jeu
    #########################################
    fenetre = pg.display.set_mode((fenetretaille))
    fenetre.fill(fenetrecouleur)
    pg.display.set_caption('Olive et le MysteryMan')

    #########################################
    # gestion du temps et des délais des listeners
    # sur les évènements claviers
    #########################################
    horloge = pg.time.Clock()
    pg.key.set_repeat(10, 50)

    score = scoreinitial
    #########################################
    # declaration des sons du jeu
    #########################################
    blip = pg.mixer.Sound('son/beep3-98810.ogg')
    #########################################
    # Création des surfaces de décors
    #########################################
    sol = pg.image.load(fichiersdecors[2]).convert_alpha()
    sol = pg.transform.scale(sol, (sol.get_width() * 2, sol.get_height() * 2))
    herbederriere = pg.image.load(fichiersdecors[0]).convert_alpha()
    herbederriere = pg.transform.scale(herbederriere, (herbederriere.get_width() * 4, herbederriere.get_height() * 4))
    herbedevant = pg.image.load(fichiersdecors[1]).convert_alpha()
    herbedevant = pg.transform.scale(herbedevant, (herbedevant.get_width() * 2, herbedevant.get_height() * 2))
    decorx = 0
    decory = 0
    #########################################
    # création des groupes de sprites
    #########################################
    listeglobalesprites = pg.sprite.Group()
    listeolivesprite = pg.sprite.Group()
    listeoliveitemssprites = pg.sprite.Group()
    listeitemssprites = pg.sprite.Group()
    #########################################
    # instanciation des sprites
    #########################################

    olivevecteurimagessprites = remplissageVecteur(fichiersolive)
    directionolive = 'D' #direction par défaut
    olivesaute = False #par défaut il ne saute pas
    oliveestchevalier = estchevalier  # False par défaut
    olive = Olive(olivevecteurimagessprites, 14)

    epeevecteurimagesprite = remplissageVecteur(fichiersepee)
    epee = Epee(epeevecteurimagesprite, 0)

    #########################################
    # remplissage des groupes de sprites
    #########################################
    listeglobalesprites.add(olive)
    listeolivesprite.add(olive)
    listeitemssprites.add(epee)
    listeglobalesprites.add(epee)

    #########################################
    # boucle principale du jeu
    #########################################
    while jeu:
        fenetre.fill(fenetrecouleur)
        # on définit le fps
        horloge.tick(60)
        pg.key.set_repeat(50, 0)
        keys = pg.key.get_pressed()

        #########################################
        # Gestion des évènements clavier
        #########################################
        for event in pg.event.get():
            if event.type == pg.QUIT:
                jeu = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    jeu = False
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_LEFT:
                    if oliveestchevalier == False :
                        directionolive = olive.deplacerGauche(4, 7)
                    else :
                        directionolive = olive.deplacerGauche(19, 20)
                    epee.scrollingdroite()
                    decorx += vitesse

                if event.key == pg.K_RIGHT:
                    if oliveestchevalier ==False :
                        directionolive = olive.deplacerDroite(0, 3)
                    else :
                        directionolive = olive.deplacerDroite(17,18)
                    epee.scrollinggauche()
                    decorx -= vitesse

        if olivesaute == False:
            if keys[pg.K_LCTRL] or keys[pg.K_SPACE]:
                olivesaute = True
        elif olivesaute == True:
            if directionolive == 'D':
                olivesaute = olive.sauter(20, 8, 8, directionolive)
            elif directionolive == 'G':
                olivesaute = olive.sauter(20, 9, 9, directionolive)

        #########################################
        # affichage des décors et éléments de sprites
        #########################################
        # en fond de décor
        if decorx <= -fenetrelargeur or decorx >= fenetrelargeur:
            decorx = 0

        fenetre.blit(herbederriere,
                     (decorx - herbederriere.get_width(), fenetrehauteur - 6 - herbederriere.get_height()))
        fenetre.blit(herbederriere, (decorx, fenetrehauteur - 6 - herbederriere.get_height()))
        fenetre.blit(herbederriere,
                     (decorx + herbederriere.get_width(), fenetrehauteur - 6 - herbederriere.get_height()))

        fenetre.blit(sol, (decorx - sol.get_width(), fenetrehauteur - sol.get_height() - 10))
        fenetre.blit(sol, (decorx, fenetrehauteur - sol.get_height() - 10))
        fenetre.blit(sol, (decorx + sol.get_width(), fenetrehauteur - sol.get_height() - 10))
        #########################################
        # Gestion des sprites et tests de collisions
        #########################################
        listecollisionsoliveepee = pg.sprite.spritecollide(olive, listeitemssprites, True)

        # on update tous les sprites et on les affiche
        listeglobalesprites.update()
        listeglobalesprites.draw(fenetre)

        # éléments de décor en avant plan
        fenetre.blit(herbedevant, (decorx - herbedevant.get_width(), fenetrehauteur - herbedevant.get_height()))
        fenetre.blit(herbedevant, (decorx, fenetrehauteur - herbedevant.get_height()))
        fenetre.blit(herbedevant, (decorx + herbedevant.get_width(), fenetrehauteur - herbedevant.get_height()))

        # Gestion des sons
        if listecollisionsoliveepee :
            oliveestchevalier = True
            blip.play(0,0,0)


        # rafraichissement de l'écran avec le delai
        pg.time.delay(10)
        pg.display.flip()


if __name__ == '__main__':
    main()