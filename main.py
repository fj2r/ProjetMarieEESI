#################################################################
#
#       Jeu en Pygame pour projet EESI
#       Graphics by Marie
#       Coding by Fred - python ver. 3.8.5 - pygame ver.
#       ver. beta-0.6
#
#################################################################
import sys, time
import pygame as pg
import pygame.freetype
from pygame.locals import *
from classes import *
from config import *
from fonctions import *
import random


def main():
    pg.mixer.pre_init(44100, 16, 2, 4096)
    pg.init()  # initialisation des modules
    pg.freetype.init()
    # pg.mixer.init()  # initialisation du mixer son
    # pg.font.init()  # initialisation des modules de police
    FPS = 30
    # #######################Constantes utiles#######################################
    fichiersmapsecrete = remplissageImagesSonsJeu("img/map_secrète/")

    jeu = jeuetatinitial  # état du jeu
    level = leveldemarrage  # level de démarrage
    ##################################################################################
    # construction de la fenêtre principale du jeu
    ##################################################################################
    fenetre = pg.display.set_mode(fenetretaille, DOUBLEBUF, 16)
    bgd = pg.display.set_mode(fenetretaille)
    fenetre.fill(fenetrecouleur)
    pg.display.set_caption("Olive et le MysteryHuMan")

    #########################################
    # gestion du temps et des délais des listeners
    # sur les évènements claviers
    #########################################
    horloge = pg.time.Clock()
    current_timer = 0
    animation_timer = timer
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
    # chargement des sons et musiques du jeu
    #########################################

    fichiersmusiques = remplissageImagesSonsJeu("son/musiques/ogg/")
    listemusiques = []

    for musique in fichiersmusiques:
        listemusiques.append(pg.mixer.Sound(musique))

    #########################################
    # declaration des polices du jeu
    #########################################
    policeurl = policepardefaut
    policebulle = policepardefaut
    #########################################
    # Création des surfaces de décors - Level 1
    #########################################
    # sol = pg.image.load(fichiersdecors[2]).convert_alpha()
    # sol = pg.transform.scale(sol, (sol.get_width() * 2, sol.get_height() * 2))
    # mapmystere = pg.image.load('img/map_mystère.png').convert_alpha()
    # mapmystere= pg.transform.scale(mapmystere, (133*1,3057*1))
    mapx = 0
    mapy = 0

    herbederriere = pg.image.load(fichiersdecors[0]).convert_alpha()
    herbederriere = pg.transform.scale2x(herbederriere)
    herbedevant = pg.image.load(fichiersdecors[1]).convert_alpha()
    herbedevant = pg.transform.scale2x(herbedevant)

    #########################################
    # Création des surfaces de décors - Level 2
    #########################################
    # sol = pg.image.load(fichiersdecors[2]).convert_alpha()
    # sol = pg.transform.scale(sol, (sol.get_width() * 2, sol.get_height() * 2))
    mapmystere = pg.image.load("img/perso mystère/map_mystère.png").convert_alpha()

    mapmysteregrossissement = fenetrelargeur // 133

    mapmystere = pg.transform.scale(
        mapmystere,
        (int(133 * mapmysteregrossissement), int(3057 * mapmysteregrossissement)),
    )
    decormapmystere = mapmystere.get_rect()
    decormapmystere.left = 0
    decormapmystere.bottom = fenetrehauteur

    mapsecretesol = pg.image.load(fichiersmapsecrete[2]).convert_alpha()
    mapsecretesol = pg.transform.scale2x(mapsecretesol)
    mapsecreteherbe = pg.image.load(fichiersmapsecrete[1]).convert_alpha()
    mapsecreteherbe = pg.transform.scale2x(mapsecreteherbe)
    mapsecreteciel = pg.image.load(fichiersmapsecrete[0]).convert_alpha()
    mapsecreteciel = pg.transform.scale2x(mapsecreteciel)

    decorx = 0
    decory = fenetrehauteur
    #########################################
    # Vecteurs des images du jeu pour les sprites
    #########################################
    """phylacteres = remplissageImagesSonsJeu("img/bulles/")
    items = remplissageImagesSonsJeu("img/items/")
    fichiersmapsecrete = remplissageImagesSonsJeu("img/map_secrète/")
    olivedeplacements = remplissageImagesSonsJeu("img/olive deplacements/")
    olivechevalier = remplissageImagesSonsJeu("img/olive_deplacemnts_armure/")
"""
    #########################################
    # création des groupes de sprites
    #########################################
    listeglobalesprites = pg.sprite.Group()
    listeolivesprites = pg.sprite.Group()
    listebullessprite = pg.sprite.Group()
    listeoliveitemssprites = pg.sprite.Group()
    listeitemssprites = pg.sprite.Group()
    listeepeesprites = pg.sprite.Group()
    listeMHcombatsprites = pg.sprite.Group()
    listeballesprites = pg.sprite.Group()
    # listeportesprites = pg.sprite.Group()
    listebriquessprites = pg.sprite.Group()
    listesolsprites = pg.sprite.Group()
    listeoeilsprites = pg.sprite.Group()
    listemysterysprites = pg.sprite.Group()
    listeboitedialoguesprites = pg.sprite.Group()

    #########################################
    # instanciation des sprites et ajout aux groupes de sprites pour les sprites répétitifs
    #########################################

    olivevecteurimagessprites = remplissageVecteur(fichiersoliveconcatenee)
    directionolive = "D"  # direction par défaut
    olive = Olive(olivevecteurimagessprites, 14)

    mysteryhumanvecteurimagessprite = remplissageVecteur(fichiersmysteryhuman)
    mysteryhuman = Mysteryhuman(mysteryhumanvecteurimagessprite, 2)

    mysteryhumancombatimagessprite = remplissageVecteur(fichiersmysteryhuman)
    mysteryhumancombat = Mysteryhuman(mysteryhumancombatimagessprite, 6)
    mysteryhumancombat.rect.right, mysteryhumancombat.rect.bottom = MHcombat_x, MHcombat_y

    bullesvecteurimagessprite = remplissageVecteur(fichiersbulles)
    bulle = Phylactere(bullesvecteurimagessprite, 1)

    ballevecteurimagessprite = remplissageVecteur(fichiersballes)
    balle = Balles(ballevecteurimagessprite, 0)

    solvecteurimagessprites = remplissageVecteur(fichiersdecors)
    sol = Sol(solvecteurimagessprites, 2)

    epeevecteurimagesprite = remplissageVecteur(fichiersepee)
    epee = Epee(epeevecteurimagesprite, 0)

    boitedialogueimagesprite = remplissageVecteur(fichierboitedialogue)
    boitedialogue = Boitedialogue(boitedialogueimagesprite, 0)

    oeilvecteurimagesprite = remplissageVecteur(fichiersoeil)
    for i in range(0, nboeil):
        oeil = Oeil(oeilvecteurimagesprite, 0)
        oeil.rect.x = listepositionyeux[i][0]
        oeil.rect.y = listepositionyeux[i][1]

        listeoeilsprites.add(oeil)
        listeglobalesprites.add(oeil)

    # portevecteurimagesprite = remplissageVecteur(fichiersportedefin)
    # porte = Porte(portevecteurimagesprite, 0)

    briquesvecteurimagessprites = remplissageVecteur(fichiersbriques)
    for i in range(0, nbbriques):
        brique = Brique(briquesvecteurimagessprites, 0)
        brique.rect.x = listepositionbriques[i][0]
        brique.rect.y = listepositionbriques[i][1]

        listebriquessprites.add(brique)
        listeglobalesprites.add(brique)
    briqueMH = Brique(briquesvecteurimagessprites, 1)
    briqueMH.rect.right, briqueMH.rect.top = MHcombat_x, MHcombat_y
    listebriquessprites.add(briqueMH)
    listeglobalesprites.add(briqueMH)
    briqueOliveCombat = Brique(briquesvecteurimagessprites, 0)
    briqueOliveCombat.rect.right, briqueOliveCombat.rect.bottom = (
        MHcombat_x ,
        MHcombat_y,
    )
    listebriquessprites.add(briqueOliveCombat)
    listeglobalesprites.add(briqueOliveCombat)

    #########################################
    # remplissage des groupes de sprites pour les sprites non répétitifs
    #########################################
    # listeglobalesprites.add(olive)
    listeolivesprites.add(olive)
    listebullessprite.add(bulle)
    listesolsprites.add(sol)
    listeitemssprites.add(epee)
    listeepeesprites.add(epee)
    # listeportesprites.add(porte)
    listemysterysprites.add(mysteryhuman)
    listeMHcombatsprites.add(mysteryhumancombat)
    listeboitedialoguesprites.add(boitedialogue)
    listeballesprites.add(balle)
    listeglobalesprites.add(epee, sol)
    #########################################
    # démarrage de la musique de début après un delay
    #########################################
    pg.time.wait(200)
    listemusiques[1].play(1, 0, 500)  # pour écran d'accueil
    #######################################################################################
    #                               boucle principale du jeu                              #
    #######################################################################################
    while jeu:
        fenetre.fill(fenetrecouleur)
        # on définit le fps

        dt = horloge.tick(FPS) / 1000
        pg.key.set_repeat(20, 0)
        keys = pg.key.get_pressed()

        #########################################
        # Gestion des vies
        #########################################
        if zonescoreetvie.vies <= 0:
            olive.level = 3
        #########################################
        # Gestion des évènements clavier - jeu entier
        #########################################

        ##################################################################################
        #                       niveau 0 - Splash screen
        ##################################################################################
        if olive.level == 0:
            pg.key.set_repeat(20, 0)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    jeu = False
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    olive.level = 1

            fenetre.fill(fenetrecouleur)
            splash = pg.image.load("img/écran titre final.png").convert_alpha()
            splash = pg.transform.scale(splash, (fenetrelargeur, fenetrehauteur))

            police1 = pg.font.Font(policeurl, taillepolice)
            police2 = pg.font.Font(policeurl, taillepolice)
            splashtexte = police1.render(
                "Appuyez sur une touche pour commencer !",
                True,
                (255, 0, 0),
                (0, 5, 255),
            )
            splashtexte2 = police2.render(
                "Appuyez sur une touche pour commencer !",
                True,
                (0, 0, 255),
                (255, 5, 0),
            )
            pg.time.wait(500)
            fenetre.blit(splash, (0, 0))
            fenetre.blit(splashtexte, (100, fenetrehauteur - 50 - taillepolice // 2))
            pg.time.delay(10)
            pg.display.flip()
            pg.time.wait(500)
            fenetre.fill(fenetrecouleur)
            fenetre.blit(splash, (0, 0))
            fenetre.blit(splashtexte2, (100, fenetrehauteur - 50 - taillepolice // 2))
            pg.time.delay(10)
            pg.display.flip()

        ############################################################################
        #                            ** niveau 1 **
        ############################################################################
        if olive.level == 1:
            olive.level = 1
            pg.key.set_repeat(20, 0)
            listemusiques = []
            current_timer += dt

            #########################################
            # Gestion des évènements clavier - level 1
            #########################################

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    jeu = False
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYUP:
                    olive.index = 0  # remise à 0 des index des frames pour les vecteurs d'animations
                    olive.entraindesauter = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        olive.level = 1

                    if event.key == pg.K_2:

                        olive.level = 2

                    if event.key == pg.K_ESCAPE:
                        jeu = False
                        pg.quit()
                        sys.exit()

                    if event.key == pg.K_LEFT:
                        if current_timer >= animation_timer:
                            if olive.estchevalier == False:
                                olive.deplacerGauche([1, 2, 3, 2, 1])
                            else:
                                olive.deplacerGauche([16, 17, 16])
                            epee.scrollingdroite()
                            # porte.scrollingdroite()
                            mysteryhuman.scrollingdroite()
                            bulle.scrollingdroite()
                            for brique in listebriquessprites:
                                brique.scrollingdroite()
                            for oeil in listeoeilsprites:
                                oeil.scrollingdroite()

                            decorx += vitesse
                            mapx += vitesse / 2
                            current_timer = 0

                    if event.key == pg.K_RIGHT:
                        if current_timer >= animation_timer:
                            if olive.estchevalier == False:
                                listeframes = [1, 2, 3, 2, 1]
                                olive.deplacerDroite(listeframes)
                            else:
                                listeframes = [16, 17, 16]
                                olive.deplacerDroite(listeframes)
                            epee.scrollinggauche()
                            # porte.scrollinggauche()
                            mysteryhuman.scrollinggauche()
                            bulle.scrollinggauche()
                            for brique in listebriquessprites:
                                brique.scrollinggauche()
                            for oeil in listeoeilsprites:
                                oeil.scrollinggauche()
                            decorx -= vitesse

                            mapx -= vitesse / 2
                            current_timer = 0

                    if olive.entraindesauter == False:
                        if event.key == pg.K_LCTRL or event.key == pg.K_SPACE:
                            olive.offset = 0
                            olive.entraindesauter = True

                if event.type == pg.KEYUP:
                    if event.key == pg.K_RETURN:
                        if bulle.indexdialogue < bulle.longueurlistedialogue:
                            bulle.indexdialogue += 1

                    if event.key == pg.K_o:
                        boitedialogue.reponse = 1
                        mysteryhuman.reponse = 1
                    if event.key == pg.K_n:
                        boitedialogue.reponse = 2
                        mysteryhuman.reponse = 2

            #########################################
            # affichage des décors et éléments de sprites
            #########################################
            fenetre.blit(
                mapmystere,
                (mapx, mapy),
            )
            affichageDecor(
                fenetre,
                decorx + herbederriere.get_width(),
                herbederriere,
                fenetrelargeur,
                fenetrehauteur,
            )
            affichageDecor(
                fenetre, decorx, herbederriere, fenetrelargeur, fenetrehauteur
            )
            affichageDecor(
                fenetre,
                decorx - herbederriere.get_width(),
                herbederriere,
                fenetrelargeur,
                fenetrehauteur,
            )

            #########################################
            # Gestion des sprites et tests de collisions
            #########################################
            """listecollisionsoliveitems = pg.sprite.spritecollide(
                olive, listeitemssprites, False
            )"""
            # position du mystery human et du phylactère :
            positionMH = (mysteryhuman.rect.x, mysteryhuman.rect.y)

            # on update tous les sprites et on les affiche
            listeglobalesprites.update()  # test de collision dans la méthode update
            listeolivesprites.update(
                listesolsprites,
                listebriquessprites,
                listeepeesprites,
                zonescoreetvie,
                listeoeilsprites,
                listemysterysprites,
                sol,
                mysteryhumancombat,
            )
            listebullessprite.update()
            listeboitedialoguesprites.update()
            listemysterysprites.update(
                listeboitedialoguesprites,
                listeolivesprites,
                listebullessprite,
                listeballesprites,
                positionMH,
                fenetre,
                boitedialogue,
                bulle,
                olive,
                zonescoreetvie,
            )

            # listeglobalesprites.draw(fenetre)
            listesolsprites.draw(fenetre)
            # listebriquessprites.draw(fenetre)
            # listeoeilsprites.draw(fenetre)
            # listeepeesprites.draw(fenetre)
            listemysterysprites.draw(fenetre)
            # listebullessprite.draw(fenetre)
            listeolivesprites.draw(fenetre)

            # éléments de décor en avant plan

            affichageDecor(
                fenetre,
                decorx - herbedevant.get_width(),
                herbedevant,
                fenetrelargeur,
                fenetrehauteur + 6,
            )
            affichageDecor(
                fenetre, decorx, herbedevant, fenetrelargeur, fenetrehauteur + 6
            )
            affichageDecor(
                fenetre,
                decorx + herbedevant.get_width(),
                herbedevant,
                fenetrelargeur,
                fenetrehauteur + 6,
            )

            if (
                decorx >= fenetrelargeur or decorx <= -fenetrelargeur
            ):  # pour redessiner les décors à l'infini lors des déplacements
                decorx = 0

            #########################################
            # affichage de la zone de score et de vies
            #########################################

            zonescoreetvie.affichagescore(fenetre)

            # Gestion des sons

            pg.time.delay(40)
            pg.display.flip()
            if mysteryhuman.findesequence == 1:
                olive.level = 2  # à la fin des dialogues on passe au niveau 2
        #############################################################################
        #                 ** Niveau 2 :  **
        #############################################################################
        if olive.level == 2:
            # listemusiques[1].stop()

            current_timer += dt
            #
            """for brique in listebriquessprites:
                brique.kill()"""
            """for oeil in listeoeilsprites:
                oeil.kill()"""
            """for epee in listeepeesprites:
                epee.kill()"""
            for mysteryhuman in listemysterysprites:
                mysteryhuman.kill()
            """for sol in listesolsprites:
                sol.kill()"""

            # sol.rect.top = fenetrehauteur - 10
            #########################################
            # Gestion des évènements clavier - level 2
            #########################################
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    jeu = False
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYUP:
                    olive.index = 0  # remise

                if event.type == pg.KEYDOWN:

                    if event.key == pg.K_1:
                        olive.level = 1
                    if event.key == pg.K_ESCAPE:
                        jeu = False
                        pg.quit()
                        sys.exit()
                    if event.key == pg.K_LEFT:
                        if olive.estchevalier == False:
                            olive.deplacerGaucheL2([1, 2, 3, 2, 1])
                        else:
                            olive.deplacerGaucheL2([16, 17, 16])
                        decorx -= 0
                    if event.key == pg.K_SPACE:
                        if olive.estchevalier == True:
                            olive.attaque([16, 18, 16])
                            mysteryhumancombat.coupporte = True

                    if event.key == pg.K_c:
                        olive.estchevalier = True
                    if event.key == pg.K_b:
                        balle.vitesse = 0
                    if event.key == pg.K_RIGHT:
                        if olive.estchevalier == False:
                            olive.deplacerDroiteL2([1, 2, 3, 2, 1])
                        else:
                            olive.deplacerDroiteL2([16, 17, 16])

                        decorx += 0

                    if olive.entraindesauterL2 == False:
                        if event.key == pg.K_LCTRL:
                            olive.offset = 0
                            olive.entraindesauterL2 = True

                    if olive.entraindesauterL2 == True:

                        mysteryhumancombat.scrollingbas(olive.offset // 2)
                        epee.scrollingbas(olive.offset // 2)
                        for brique in listebriquessprites:
                            brique.scrollingbas(olive.offset // 2)
                        for oeil in listeoeilsprites:
                            oeil.scrollingbas(olive.offset // 2)
                        sol.rect.y += olive.offset // 2

                        decory += olive.decory * 2

                    else:

                        decorx += 0
                        decory -= 0

            #########################################
            # affichage des décors et éléments de sprites
            #########################################
            fenetre.blit(
                mapmystere,
                (
                    0,
                    -3000 * mapmysteregrossissement + fenetrehauteur * 5 - olive.decory,
                ),
            )
            affichageDecorL2(
                fenetre,
                decorx - herbedevant.get_width(),
                herbedevant,
                fenetrelargeur,
                fenetrehauteur + 6,
                decory,
                olive.offset,
            )
            affichageDecorL2(
                fenetre,
                decorx,
                herbedevant,
                fenetrelargeur,
                fenetrehauteur + 6,
                decory,
                olive.offset,
            )
            affichageDecorL2(
                fenetre,
                decorx + herbedevant.get_width(),
                herbedevant,
                fenetrelargeur,
                fenetrehauteur + 6,
                decory,
                olive.offset,
            )

            #########################################
            # Gestion des sprites et tests de collisions
            #########################################
            """listecollisionsoliveitems = pg.sprite.spritecollide(
                olive, listeitemssprites, False
            )"""
            # position du mystery human et du phylactère :
            positionMH = (mysteryhuman.rect.x, mysteryhuman.rect.y)

            # on update tous les sprites et on les affiche
            listeglobalesprites.update()  # test de collision dans la méthode update
            listeolivesprites.update(
                listesolsprites,
                listebriquessprites,
                listeepeesprites,
                zonescoreetvie,
                listeoeilsprites,
                listemysterysprites,
                sol,
                mysteryhumancombat,
            )
            listebullessprite.update()
            listeboitedialoguesprites.update()

            listeMHcombatsprites.update(
                listeboitedialoguesprites,
                listeolivesprites,
                listebullessprite,
                listeballesprites,
                positionMH,
                fenetre,
                boitedialogue,
                bulle,
                olive,
                zonescoreetvie,
            )

            # listeglobalesprites.draw(fenetre)
            listesolsprites.draw(fenetre)
            listebriquessprites.draw(fenetre)
            listeoeilsprites.draw(fenetre)
            listeepeesprites.draw(fenetre)
            listeMHcombatsprites.draw(fenetre)
            # listebullessprite.draw(fenetre)
            listeolivesprites.draw(fenetre)
            # éléments de décor en avant plan
            fenetre.blit(
                herbedevant,
                (
                    decorx - herbedevant.get_width(),
                    fenetrehauteur - herbedevant.get_height() - decory,
                ),
            )
            fenetre.blit(
                herbedevant,
                (decorx, fenetrehauteur - herbedevant.get_height() - decory),
            )
            fenetre.blit(
                herbedevant,
                (
                    decorx + herbedevant.get_width(),
                    fenetrehauteur - herbedevant.get_height() - decory,
                ),
            )
            #########################################
            # affichage de la zone de score et de vies
            #########################################

            zonescoreetvie.affichagescore(fenetre)

            # Gestion des sons

            pg.time.delay(40)
            pg.display.flip()
        ##################################################################################
        #                       niveau 3 - Splash screen de fin
        ##################################################################################
        if olive.level == 3:
            pg.key.set_repeat(20, 0)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    jeu = False
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    olive.level = 1

            fenetre.fill(fenetrecouleur)
            splash = pg.image.load("img/écran titre final.png").convert_alpha()
            splash = pg.transform.scale(splash, (fenetrelargeur, fenetrehauteur))

            police1 = pg.font.Font(policeurl, taillepolice * 4)
            police2 = pg.font.Font(policeurl, taillepolice * 4)
            splashtexte = police1.render(
                "GAME OVER !",
                True,
                (255, 0, 0),
                (0, 5, 255),
            )
            splashtexte2 = police2.render(
                "GAME OVER !",
                True,
                (0, 0, 255),
                (255, 5, 0),
            )
            pg.time.wait(500)
            fenetre.blit(splash, (0, 0))
            fenetre.blit(splashtexte, (200, fenetrehauteur - 200 - taillepolice // 2))
            pg.time.delay(10)
            pg.display.flip()
            pg.time.wait(500)
            fenetre.fill(fenetrecouleur)
            fenetre.blit(splash, (0, 0))
            fenetre.blit(splashtexte2, (200, fenetrehauteur - 200 - taillepolice // 2))
            pg.time.delay(10)
            pg.display.flip()


if __name__ == "__main__":
    main()
