#################################################################
#
#       Jeu en Pygame pour projet EESI
#       Graphics by Marie
#       Coding by Fred - python ver. 3.8.5
#       ver. alpha-0.5
#
#################################################################
import sys, time
import pygame as pg
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
    pg.display.set_caption("Olive et le MysteryHuMan")

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
    #########################################
    # Création des surfaces de décors
    #########################################
    #sol = pg.image.load(fichiersdecors[2]).convert_alpha()
    #sol = pg.transform.scale(sol, (sol.get_width() * 2, sol.get_height() * 2))
    mapmystere = pg.image.load('img/map_mystère.png').convert_alpha()
    mapmystere = pg.transform.scale(mapmystere, (133*6,3057*6))
    mapx = 0
    mapy = 0

    herbederriere = pg.image.load(fichiersdecors[0]).convert_alpha()
    herbederriere = pg.transform.scale2x(
        herbederriere
    )
    herbedevant = pg.image.load(fichiersdecors[1]).convert_alpha()
    herbedevant = pg.transform.scale2x(
        herbedevant
    )
    decorx = 0
    decory = 0
    #########################################
    # Vecteurs des images du jeu pour les sprites
    #########################################
    phylacteres = remplissageImagesSonsJeu("img/bulles/")
    items = remplissageImagesSonsJeu("img/items/")
    fichiersmapsecrete = remplissageImagesSonsJeu("img/map_secrète/")
    olivedeplacements = remplissageImagesSonsJeu("img/olive deplacements/")
    olivechevalier = remplissageImagesSonsJeu("img/olive_deplacemnts_armure/")

    #########################################
    # création des groupes de sprites
    #########################################
    listeglobalesprites = pg.sprite.Group()
    listeolivesprite = pg.sprite.Group()
    listebullessprite = pg.sprite.Group()
    listeoliveitemssprites = pg.sprite.Group()
    listeitemssprites = pg.sprite.Group()
    listeepeesprites = pg.sprite.Group()
    listebriquessprites = pg.sprite.Group()
    listesolsprites = pg.sprite.Group()

    #########################################
    # instanciation des sprites
    #########################################

    olivevecteurimagessprites = remplissageVecteur(fichiersoliveconcatenee)
    directionolive = "D"  # direction par défaut
    olive = Olive(olivevecteurimagessprites, 14)

    bullesvecteurimagessprite = remplissageVecteur(fichiersbulles)
    bulle = Phylactere(bullesvecteurimagessprite, 0)

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
    listebullessprite.add(bulle)
    listeglobalesprites.add(bulle)
    listesolsprites.add(sol)
    listeglobalesprites.add(sol)
    listeitemssprites.add(epee)
    listeglobalesprites.add(epee)
    listeepeesprites.add(epee)
    listeglobalesprites.add(brique)
    listebriquessprites.add(brique)

    #########################################
    # démarrage de la musique de début après un delay
    #########################################
    pg.time.wait(500)
    listemusiques[5].play(0, 0, 500)  # pour écran d'accueil
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
        # Gestion des évènements clavier - jeu entier
        #########################################


        #########################################
        # niveau 0 - Splash screen
        #########################################
        if level == 0:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    jeu = False
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    level = 1

            fenetre.fill(fenetrecouleur)
            splash = pg.image.load('img/écran titre final.png').convert_alpha()
            splash = pg.transform.scale(splash, (fenetrelargeur,fenetrehauteur))

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
            fenetre.blit(splash, (0,0))
            fenetre.blit(splashtexte, (100, fenetrehauteur -50 - taillepolice // 2))
            pg.time.delay(10)
            pg.display.flip()
            pg.time.wait(500)
            fenetre.fill(fenetrecouleur)
            fenetre.blit(splash, (0, 0))
            fenetre.blit(splashtexte2, (100, fenetrehauteur -50 - taillepolice // 2))
            pg.time.delay(10)
            pg.display.flip()
############################################################################
#                 ** niveau 1 **
############################################################################
        if level == 1:
            listemusiques[5].stop()

            #########################################
            # Gestion des évènements clavier - level 1
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
                        if olive.estchevalier == False:
                            olive.deplacerGauche([1,2,3,2,1])
                        else:
                            olive.deplacerGauche([16,17,16])
                        epee.scrollingdroite()
                        brique.scrollingdroite()
                        decorx += vitesse
                        mapx += vitesse/2

                    if event.key == pg.K_RIGHT:
                        if olive.estchevalier == False:
                            listeframes = ([1,2,3,2,1])
                            olive.deplacerDroite(listeframes)
                        else:
                            listeframes = ([16,17,16])
                            olive.deplacerDroite(listeframes)
                        epee.scrollinggauche()
                        brique.scrollinggauche()
                        decorx -= vitesse
                        mapx -= vitesse/2

                    if olive.entraindesauter == False :
                        if event.key == pg.K_LCTRL :
                            olive.entraindesauter = True



            #########################################
            # affichage des décors et éléments de sprites
            #########################################
            fenetre.blit(
                mapmystere,
                (
                    mapx,
                    mapy
                ),
            )
            affichageDecor(fenetre, decorx+herbederriere.get_width(), herbederriere, fenetrelargeur, fenetrehauteur)
            affichageDecor(fenetre, decorx, herbederriere, fenetrelargeur, fenetrehauteur)
            affichageDecor(fenetre, decorx-herbederriere.get_width(), herbederriere, fenetrelargeur, fenetrehauteur)

            #########################################
            # Gestion des sprites et tests de collisions
            #########################################

            listecollisionsoliveitems = pg.sprite.spritecollide(
                olive, listeitemssprites, False
            )



            # on update tous les sprites et on les affiche
            listeglobalesprites.update()
            listeolivesprite.update(listesolsprites, listebriquessprites, listeepeesprites, zonescoreetvie)



            listeglobalesprites.draw(fenetre)
            listeolivesprite.draw(fenetre)

            # éléments de décor en avant plan

            affichageDecor(fenetre, decorx-herbedevant.get_width(), herbedevant, fenetrelargeur, fenetrehauteur+6)
            affichageDecor(fenetre, decorx, herbedevant, fenetrelargeur, fenetrehauteur+6)
            affichageDecor(fenetre, decorx+herbedevant.get_width(), herbedevant, fenetrelargeur, fenetrehauteur+6)

            if decorx >= fenetrelargeur or decorx <= -fenetrelargeur : # pour redessiner les décors à l'infini lors des déplacements
                decorx = 0
            #########################################
            # affichage de la zone de score et de vies
            #########################################


            zonescoreetvie.affichagescore(fenetre)

            # Gestion des sons

            pg.time.delay(40)
            pg.display.flip()
#############################################################################
#                 ** Niveau 2 **
#############################################################################
        if level == 2:
            listemusiques[5].stop()

            #########################################
            # Gestion des évènements clavier - level 2
            #########################################
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:

                    if event.key == pg.K_ESCAPE:
                        jeu = False
                        pg.quit()
                        sys.exit()
                    if event.key == pg.K_LEFT:
                        if olive.estchevalier == False:
                            olive.deplacerGauche(5, 7)
                        else:
                            olive.deplacerGauche(0, 21)
                        epee.scrollingdroite()
                        brique.scrollingdroite()
                        decorx += vitesse
                        mapx += vitesse/2

                    if event.key == pg.K_RIGHT:
                        if olive.estchevalier == False:
                            olive.deplacerDroite(1, 3)
                        else:
                            olive.deplacerDroite(5, 7)
                        epee.scrollinggauche()
                        brique.scrollinggauche()
                        decorx -= vitesse
                        mapx -= vitesse/2

                    if olive.entraindesauter == False :
                        if event.key == pg.K_LCTRL :
                            olive.entraindesauter = True



            #########################################
            # affichage des décors et éléments de sprites
            #########################################
            fenetre.blit(
                mapmystere,
                (
                    mapx,
                    mapy
                ),
            )
            affichageDecor(fenetre, decorx, herbederriere, fenetrelargeur, fenetrehauteur)

            #########################################
            # Gestion des sprites et tests de collisions
            #########################################

            listecollisionsoliveitems = pg.sprite.spritecollide(
                olive, listeitemssprites, False
            )



            # on update tous les sprites et on les affiche
            listeglobalesprites.update()
            listeolivesprite.update(listesolsprites, listebriquessprites, listeepeesprites, zonescoreetvie)



            listeglobalesprites.draw(fenetre)
            listeolivesprite.draw(fenetre)

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

            pg.time.delay(40)
            pg.display.flip()
        if level == 3:
            pass



if __name__ == "__main__":
    main()
