#################################################################
#
#       Jeu en Pygame pour projet EESI
#       Graphics by Marie
#       Coding by Fred - python ver. 3.8.5
#       ver. alpha-0.4
#
#################################################################
import sys

from classes import *
from conf import *
from fonctions import *


def main():
    pg.init()  # initialisation des modules
    pg.mixer.init()  # initialisation du mixer son
    pg.font.init()  # initialisation des modules de police

    jeu = jeuetatinitial
    level = leveldemarrage
    #########################################
    # définition de la fenetre principale du jeu
    #########################################
    fenetre = pg.display.set_mode(fenetretaille)
    fenetre.fill(fenetrecouleur)
    pg.display.set_caption("Olive et le MysteryMan")

    #########################################
    # gestion du temps et des délais des listeners
    # sur les évènements claviers
    #########################################
    horloge = pg.time.Clock()
    pg.key.set_repeat(0, 0)

    #########################################
    # init des valeurs de score + vie
    #########################################
    score = scoreinitial
    vieolive = vieoliveinitiale
    iterateurscore = 0
    zonescoreetvie = AffichageScoreVies(
        fenetre, vieoliveinitiale, score, iterateurscore
    )

    #########################################
    # declaration des sons du jeu
    #########################################


    #########################################
    # declaration des polices du jeu
    #########################################
    policeurl = policepardefaut
    #########################################
    # Création des surfaces de décors
    #########################################
    #sol = pg.image.load(fichiersdecors[2]).convert_alpha()
    #sol = pg.transform.scale(sol, (sol.get_width() * 2, sol.get_height() * 2))
    herbederriere = pg.image.load(fichiersdecors[0]).convert_alpha()
    herbederriere = pg.transform.scale(
        herbederriere, (herbederriere.get_width() * 4, herbederriere.get_height() * 4)
    )
    herbedevant = pg.image.load(fichiersdecors[1]).convert_alpha()
    herbedevant = pg.transform.scale(
        herbedevant, (herbedevant.get_width() * 2, herbedevant.get_height() * 2)
    )
    decorx = 0
    decory = 0
    #########################################
    # création des groupes de sprites
    #########################################
    listeglobalesprites = pg.sprite.Group()
    listeolivesprite = pg.sprite.Group()
    listeoliveitemssprites = pg.sprite.Group()
    listeitemssprites = pg.sprite.Group()
    listeepeesprites = pg.sprite.Group()
    listebriquessprites = pg.sprite.Group()
    listesolsprites = pg.sprite.Group()

    #########################################
    # instanciation des sprites
    #########################################

    olivevecteurimagessprites = remplissageVecteur(fichiersolive)
    directionolive = "D"  # direction par défaut

    oliveestchevalier = estchevalier  # False par défaut
    olive = Olive(olivevecteurimagessprites, 14)


    solvecteurimagessprites = remplissageVecteur(fichiersdecors)
    sol = Sol(solvecteurimagessprites, 2)

    epeevecteurimagesprite = remplissageVecteur(fichiersepee)
    epee = Epee(epeevecteurimagesprite, 0)

    briquesvecteurimagessprites = remplissageVecteur(fichiersbriques)
    brique = Brique(briquesvecteurimagessprites, 0)
    #########################################
    # remplissage des groupes de sprites
    #########################################
    #listeglobalesprites.add(olive)
    listeolivesprite.add(olive)
    listesolsprites.add(sol)
    listeglobalesprites.add(sol)
    listeitemssprites.add(epee)
    listeglobalesprites.add(epee)
    listeepeesprites.add(epee)
    listeglobalesprites.add(brique)
    listebriquessprites.add(brique)

    #######################################################################################
    #                               boucle principale du jeu
    #######################################################################################
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
                if event.key == pg.K_RETURN or pg.K_KP_ENTER:
                    level = 1
                if event.key == pg.K_ESCAPE:
                    jeu = False
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_LEFT:
                    if oliveestchevalier == False:
                        directionolive = olive.deplacerGauche(4, 7)
                    else:
                        directionolive = olive.deplacerGauche(19, 20)
                    epee.scrollingdroite()
                    brique.scrollingdroite()
                    decorx += vitesse

                if event.key == pg.K_RIGHT:
                    if oliveestchevalier == False:
                        directionolive = olive.deplacerDroite(0, 3)
                    else:
                        directionolive = olive.deplacerDroite(17, 18)
                    epee.scrollinggauche()
                    brique.scrollinggauche()
                    decorx -= vitesse

        if keys[pg.K_LCTRL] or keys[pg.K_SPACE]  :

            if not olive.entraindesauter:
                olive.entraindesauter = True
                #olive.sauter( 20,listesolsprites)


        #########################################
        # niveau 0 - Splash screen
        #########################################
        if level == 0:
            fenetre.fill(fenetrecouleur)
            police1 = pg.font.Font(policeurl, taillepolice)
            police2 = pg.font.Font(policeurl, taillepolice)
            splashtexte = police1.render(
                "Appuyez sur la touche ENTREE pour démarrer !",
                True,
                (255, 0, 0),
                (0, 5, 255),
            )
            splashtexte2 = police2.render(
                "Appuyez sur la touche ENTREE pour démarrer !",
                True,
                (0, 0, 255),
                (255, 5, 0),
            )
            pg.time.wait(500)
            fenetre.blit(splashtexte, (10, fenetrehauteur // 2 - taillepolice // 2))
            pg.time.delay(10)
            pg.display.flip()
            pg.time.wait(500)
            fenetre.fill(fenetrecouleur)
            fenetre.blit(splashtexte2, (10, fenetrehauteur // 2 - taillepolice // 2))
            pg.time.delay(10)
            pg.display.flip()
        #########################################
        # niveau 1
        #########################################
        if level == 1:

            #########################################
            # affichage des décors et éléments de sprites
            #########################################
            affichageDecor(fenetre, decorx, herbederriere)

            #########################################
            # Gestion des sprites et tests de collisions
            #########################################

            listecollisionsoliveitems = pg.sprite.spritecollide(
                olive, listeitemssprites, False
            )



            # on update tous les sprites et on les affiche
            listeolivesprite.update(listesolsprites, listebriquessprites, listeepeesprites, zonescoreetvie)
            listeglobalesprites.update()

            listeolivesprite.draw(fenetre)
            listeglobalesprites.draw(fenetre)

            # éléments de décor en avant plan
            fenetre.blit(
                herbedevant,
                (
                    decorx - herbedevant.get_width(),
                    fenetrehauteur - herbedevant.get_height(),
                ),
            )
            fenetre.blit(
                herbedevant, (decorx, fenetrehauteur - herbedevant.get_height())
            )
            fenetre.blit(
                herbedevant,
                (
                    decorx + herbedevant.get_width(),
                    fenetrehauteur - herbedevant.get_height(),
                ),
            )
            #########################################
            # affichage de la zone de score et de vies
            #########################################


            zonescoreetvie.affichagescore(fenetre)

            # Gestion des sons

            pg.time.delay(50)
            pg.display.flip()
        if level == 2:
            pass
        if level == 3:
            pass



if __name__ == "__main__":
    main()
