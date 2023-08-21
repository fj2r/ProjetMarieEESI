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
        self.image = pg.transform.scale(
            self.image, (self.image.get_width() * 2, self.image.get_height() * 2)
        )
        self.rect = self.image.get_rect()
        self.rect.h = self.image.get_height()
        self.rect.w = self.image.get_width()
        self.timer = 0
        self.blip = []
        for son in fichierssons:

            self.blip.append(pg.mixer.Sound(son))


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
        self.rect.bottom = fenetrehauteur - 12
        self.rect.h = self.image.get_height() - 88

    def scrollinggauche(self):
        self.rect.move_ip(-vitesse, 0)

    def scrollingdroite(self):
        self.rect.move_ip(vitesse, 0)


class Olive(Objet):
    """
    :type Objet
    :arg Vecteur avec les fichiers pour afficher les animations du sprite
    """

    def __init__(self, image, indexdefaut):
        Objet.__init__(self, image, indexdefaut)
        self.rect.top = 0
        self.rect.left = (fenetrelargeur - self.rect.w) // 10
        self.hauteursaut = hauteursaut
        self.direction = "D"
        self.entraindesauter = False
        self.entraindetomber = True
        self.iterateur = 0
        self.estchevalier = estchevalier
        self.framedelai = self.timer
        self.signe = 1

    def update(
        self, listesolsprites, listebriquessprites, listeepeesprites, zonescoreetvie
    ):

        listecollisionsoliveepee = pg.sprite.spritecollide(self, listeepeesprites, True)
        if listecollisionsoliveepee:
            self.estchevalier = True
            self.blip[0].play(0, 0, 0)

            zonescoreetvie.calculScore(20)



        self.gravite(listesolsprites, listebriquessprites)

        if self.entraindesauter == True :
            self.sauter(10, listesolsprites)

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
        self.image = pg.transform.scale(
            self.image, (self.image.get_width() * 2, self.image.get_height() * 2)
        )

        self.index += 1
        self.iterateur += 1
        # pg.time.wait(20)

    def sauter(self, hauteursautmax, listesolsprites):

        if self.entraindesauter == True:
            if self.direction == "D":
                self.mouvementsAnimations(8, 8)
            if self.direction == "G":
                self.mouvementsAnimations(9, 9)

            self.offset = int(self.hauteursaut**2 * 0.2 * self.signe)

            self.hauteursaut -= 1
            self.rect.y -= self.offset

            print(self.rect.y)

            if self.hauteursaut < 0:
                self.signe = -self.signe

            if self.hauteursaut <= -hauteursautmax:
                self.entraindesauter = False
                self.signe = 1
                self.hauteursaut = hauteursautmax

    def gravite(self, listesolsprites, listebriquessprites):

        listecollisionsolivesbriques = pg.sprite.spritecollide(
            self, listebriquessprites, False
        )
        listecollisionsolivesol = pg.sprite.spritecollide(self, listesolsprites, False)

        if listecollisionsolivesbriques:
            if self.entraindesauter == False:
                for brique in listecollisionsolivesbriques :

                    self.rect.move_ip(0, 0)
                    if self.direction =='D' :
                        self.mouvementsAnimations(3, 3)
                    else :
                        self.mouvementsAnimations(7, 7)


        elif listecollisionsolivesol:
            if self.entraindesauter == False:

                self.rect.move_ip(0, 0)
                self.mouvementsAnimations(14,14)

        else :
            if  self.entraindesauter == False :

                self.rect.move_ip(0, 3)



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
        fenetre.blit(self.viesolive, (fenetrelargeur - 100, 20))
