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
    pg.init()           # initialisation des modules
    pg.mixer.init()     # initialisation du mixer son
    pg.font.init()      # initialisation des modules de police

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
    pg.key.set_repeat(10, 50)

    #########################################
    # init des valeurs de score + vie
    #########################################
    score = scoreinitial
    vieolive = vieoliveinitiale
    iterateurscore = 0
    zonescoreetvie = AffichageScoreVies(fenetre, vieoliveinitiale, score, iterateurscore)

    #########################################
    # declaration des sons du jeu
    #########################################
    blip = pg.mixer.Sound("son/beep3-98810.ogg")

    #########################################
    # declaration des polices du jeu
    #########################################
    policeurl = policepardefaut
    #########################################
    # Création des surfaces de décors
    #########################################
    sol = pg.image.load(fichiersdecors[2]).convert_alpha()
    sol = pg.transform.scale(sol, (sol.get_width() * 2, sol.get_height() * 2))
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

    #########################################
    # instanciation des sprites
    #########################################

    olivevecteurimagessprites = remplissageVecteur(fichiersolive)
    directionolive = "D"  # direction par défaut
    olivesaute = False  # par défaut il ne saute pas
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
    listeepeesprites.add(epee)

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
                if event.key == pg.K_RETURN or pg.K_KP_ENTER :
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
                    decorx += vitesse

                if event.key == pg.K_RIGHT:
                    if oliveestchevalier == False:
                        directionolive = olive.deplacerDroite(0, 3)
                    else:
                        directionolive = olive.deplacerDroite(17, 18)
                    epee.scrollinggauche()
                    decorx -= vitesse

        if olivesaute == False:
            if keys[pg.K_LCTRL] or keys[pg.K_SPACE]:
                olivesaute = True
        elif olivesaute == True:
            if directionolive == "D":
                olivesaute = olive.sauter(20, 8, 8, directionolive)
            elif directionolive == "G":
                olivesaute = olive.sauter(20, 9, 9, directionolive)
        #########################################
        # niveau 0 - Splash screen
        #########################################
        if level == 0 :
            fenetre.fill(fenetrecouleur)
            police1 = pg.font.Font(policeurl, taillepolice)
            police2 = pg.font.Font(policeurl, taillepolice)
            splashtexte = police1.render(
                "Appuyez sur la touche ENTREE pour démarrer !", True, (255, 0, 0), (0, 5, 255)
            )
            splashtexte2 = police2.render(
                "Appuyez sur la touche ENTREE pour démarrer !", True, (0, 0, 255), (255, 5, 0)
            )
            pg.time.wait(500)
            fenetre.blit(splashtexte, (10, fenetrehauteur//2-taillepolice//2))
            pg.time.delay(10)
            pg.display.flip()
            pg.time.wait(500)
            fenetre.fill(fenetrecouleur)
            fenetre.blit(splashtexte2, (10, fenetrehauteur//2-taillepolice//2))
            pg.time.delay(10)
            pg.display.flip()
        #########################################
        # niveau 1
        #########################################
        if level == 1:



            #########################################
            # affichage des décors et éléments de sprites
            #########################################
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

            fenetre.blit(
                sol, (decorx - sol.get_width(), fenetrehauteur - sol.get_height() - 10)
            )
            fenetre.blit(sol, (decorx, fenetrehauteur - sol.get_height() - 10))
            fenetre.blit(
                sol, (decorx + sol.get_width(), fenetrehauteur - sol.get_height() - 10)
            )
            #########################################
            # Gestion des sprites et tests de collisions
            #########################################
            listecollisionsoliveepee = pg.sprite.spritecollide(
                olive, listeepeesprites, True
            )
            listecollisionsoliveitems = pg.sprite.spritecollide(
                olive, listeitemssprites, False
            )

            # on update tous les sprites et on les affiche
            listeglobalesprites.update()
            listeglobalesprites.draw(fenetre)

            # éléments de décor en avant plan
            fenetre.blit(
                herbedevant,
                (
                    decorx - herbedevant.get_width(),
                    fenetrehauteur - herbedevant.get_height(),
                ),
            )
            fenetre.blit(herbedevant, (decorx, fenetrehauteur - herbedevant.get_height()))
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
            if listecollisionsoliveepee :
                zonescoreetvie.calculScore(20)

            zonescoreetvie.affichagescore(fenetre)

            # Gestion des sons
            if listecollisionsoliveepee:
                oliveestchevalier = True
                blip.play(0, 0, 0)
            pg.time.delay(10)
            pg.display.flip()
        if level == 2 :
            pass
        if level == 3 :
            pass
        # rafraichissement de l'écran avec le délai



if __name__ == "__main__":
    main()
