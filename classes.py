import pygame as pg
import pygame.sprite
from conf import *


class Objet(pygame.sprite.Sprite):
    """Classe parent qui hérite de la classe
    Sprite.
    Sert à instancier des objets de type Rect.
    :return None"""

    def __init__(self, image, indexdefaut):
        pygame.sprite.Sprite.__init__(self)
        self.listeimagespouranimation = []
        self.index = 0
        for element in image:
            self.listeimagespouranimation.append(
                pygame.image.load(element).convert_alpha()
            )

        self.image = self.listeimagespouranimation[indexdefaut]
        self.image.set_colorkey(couleurtransparente)
        self.image = pg.transform.scale2x(
             self.image
        )
        self.rect = self.image.get_rect()
        self.rect.h = self.image.get_height()
        self.rect.w = self.image.get_width()
        self.timer = 0
        self.cstgravitaire = gravite
        self.listesfx = []
        for sfx in fichierssons:
            self.listesfx.append(pg.mixer.Sound(sfx))



class Olive(Objet):
    """
    : type Objet
    :arg Vecteur avec les fichiers pour afficher les animations du sprite
    """

    def __init__(self, image, indexdefaut):
        Objet.__init__(self, image, indexdefaut)
        self.rect.y = 300
        self.offset = 0
        self.rect.left = (fenetrelargeur - self.rect.w) // 10
        self.hauteursaut = hauteursaut
        self.direction = "D"
        self.entraindesauter = False
        self.entraindetomber = False
        self.sautinterrompu = False
        self.iterateur = 0
        self.estchevalier = estchevalier
        self.framedelai = self.timer
        self.signe = 1
        self.cstgravitaire = gravite

    def gravite(self, gravite):
        self.rect.y += gravite

    def update(
        self, listesolsprites, listebriquessprites, listeepeesprites, zonescoreetvie
    ):

        listecollisionsolivesbriques = pg.sprite.spritecollide(
            self, listebriquessprites, False
        )
        listecollisionsoliveepee = pg.sprite.spritecollide(
            self, listeepeesprites, True
        )
        listecollisionsolivesol = pg.sprite.spritecollide(
            self, listesolsprites, False
        )
        ##################################################"
        if listecollisionsolivesbriques:
            print("collision brique")
            for brique in listecollisionsolivesbriques:

                self.rect.bottom = brique.rect.y+0
                self.sautinterrompu = True

            self.cstgravitaire = 0

        else :
            self.cstgravitaire = gravite

        if listecollisionsolivesol:
            print("collision sol")
            for sol in listecollisionsolivesol:
                self.rect.bottom = sol.rect.y+1

            self.cstgravitaire = 0
            #self.entraindesauter = False
            # self.entraindetomber = False
        else :
            self.cstgravitaire = gravite

        if self.entraindesauter == True:
            self.sauter(hauteursaut)

        self.gravite(self.cstgravitaire)
        print(self.cstgravitaire)


        if listecollisionsoliveepee:
            print("voila il a l'épée !")
            self.estchevalier = True
            self.listesfx[0].play(0, 0, 0)
            zonescoreetvie.calculScore(20)

    def deplacerGauche(self, indexdepart, indexarret):

        if self.framedelai <= 0:
            self.mouvementsAnimations(indexdepart, indexarret)
        # self.timer -= 1
        if self.rect.x < (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(-vitesse, 0)
        if self.rect.x >= (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(0, 0)
        self.direction = "G"
        return "G"

    def deplacerDroite(self, indexdepart, indexarret):

        if self.framedelai <= 0:
            self.mouvementsAnimations(indexdepart, indexarret)

        if self.rect.x < (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(vitesse, 0)
        if self.rect.x >= (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(0, 0)
        self.direction = "D"
        return "D"

    def mouvementsAnimations(self, indexdepart, indexarret):
        self.index = indexdepart + self.iterateur
        self.arretindex = indexarret

        if self.index >= self.arretindex:
            self.iterateur = 0
            self.index = indexdepart
        self.image = self.listeimagespouranimation[self.index]
        self.image.set_colorkey(couleurtransparente)
        self.image = pg.transform.scale2x(
            self.image
        )

        self.index += 1
        self.iterateur += 1
        # pg.time.wait(20)

    def sauter(self, hauteursautmax):

        if self.entraindesauter == True:
            if self.direction == "D":
                if self.estchevalier == False :
                    self.mouvementsAnimations(8, 8)
                else :
                    self.mouvementsAnimations(19, 19)
            if self.direction == "G":
                if self.estchevalier == False :
                    self.mouvementsAnimations(9, 9)
                else :
                    self.mouvementsAnimations(24, 24)


            self.offset = int(self.hauteursaut**2 * (1/2) * self.signe)


            self.rect.y -= self.offset
            self.hauteursaut -= 1

            if self.hauteursaut < 0:
                self.signe = -1
                self.entraindetomber = True

            if self.hauteursaut == -hauteursautmax-1:

                self.entraindesauter = False
                self.entraindetomber = False
                self.signe = 1
                self.hauteursaut = hauteursautmax

        if self.sautinterrompu == True and self.entraindetomber == True :
            self.entraindesauter = False
            self.entraindetomber = False
            self.offset = 0
            self.signe = 1
            self.hauteursaut = hauteursautmax



class Mysteryhuman(Objet):
    def __init__(self, image, indexdefaut):
        Objet.__init__(self , image, indexdefaut)
        self.rect.x, self.rect.y = 2000, 400
        self.vies = 1
        self.dommages = 1


class Epee(Objet):
    def __init__(self, images, indexdefaut):
        Objet.__init__(self, images, indexdefaut)
        self.rect.left = 2000
        self.rect.bottom = fenetrehauteur - 6

    def scrollinggauche(self):
        self.rect.move_ip(-vitesse, 0)

    def scrollingdroite(self):
        self.rect.move_ip(vitesse, 0)


class Sol(Objet):
    def __init__(self, image, indexdefaut):
        Objet.__init__(self, image, indexdefaut)
        self.rect.left = 0
        self.rect.y = fenetrehauteur - 20

    def scrollinggauche(self):
        self.rect.move_ip(-vitesse, 0)

    def scrollingdroite(self):
        self.rect.move_ip(vitesse, 0)


class Brique(Objet):
    def __init__(self, image, indexdefaut):
        Objet.__init__(self, image, indexdefaut)
        self.rect.bottom = (fenetrehauteur // 2) + 50
        self.rect.right = fenetrelargeur

    def scrollinggauche(self):
        self.rect.move_ip(-vitesse, 0)

    def scrollingdroite(self):
        self.rect.move_ip(vitesse, 0)


class AffichageScoreVies(pygame.font.Font):
    def __init__(self, fenetre, vies, score, iterateur):
        pygame.font.Font.__init__(self)
        self.policescore = pg.font.Font(policepardefaut, 24)
        self.policeviesolive = pg.font.Font(policepardefaut, 24)
        self.vies = vies
        self.score = score
        self.iterateur = iterateur

    def calculScore(self, gain):
        self.score += gain
        self.iterateur += 1

    def perteVies(self):
        self.vies -= 1
        return self.vies

    def gainVies(self):
        self.vies += 1
        return self.vies

    def affichagescore(self, fenetre):
        barredevie = ""
        for i in range(0, self.vies, 1):
            barredevie = barredevie + "|"
        self.scoreolive = self.policescore.render(
            "Score : %s" % self.score, 0, (255, 255, 255)
        )
        self.viesolive = self.policeviesolive.render(
            "Santé : %s" % barredevie, 0, (255, 255, 255)
        )
        fenetre.blit(self.scoreolive, (20, 20))
        fenetre.blit(self.viesolive, (fenetrelargeur - 150, 20))
