import pygame as pg
import pygame.sprite
from fonctions import *
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


class Epee(Objet):
    def __init__(self, images, indexdefaut):
        Objet.__init__(self, images, indexdefaut)
        self.rect.left = 600
        self.rect.bottom = fenetrehauteur - 6

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
        self.rect.bottom = fenetrehauteur - 6
        self.rect.left = (fenetrelargeur - self.rect.w) // 10
        self.hauteursaut = hauteursaut
        self.entraindesauter = False
        self.iterateur = 0
        self.estchevalier = estchevalier

    def deplacerGauche(self, indexdepart, indexarret):
        self.framedelai = self.timer
        if self.framedelai <= 0:
            self.mouvementsAnimations(indexdepart, indexarret)
        self.timer -= 1
        if self.rect.x < (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(-vitesse, 0)
        if self.rect.x >= (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(0, 0)
        return "G"

    def deplacerDroite(self, indexdepart, indexarret):
        self.framedelai = self.timer
        if self.framedelai <= 0:
            self.mouvementsAnimations(indexdepart, indexarret)

        if self.rect.x < (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(vitesse, 0)
        if self.rect.x >= (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(0, 0)

        return "D"

    def mouvementsAnimations(self, indexdepart, indexarret):
        self.index = indexdepart + self.iterateur
        self.arretindex = indexarret

        # print(self.index)
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
        pg.time.wait(20)

    def sauter(self, hauteursaut, indexdepart, indexarret, directionsaut):

        self.mouvementsAnimations(indexdepart, indexarret)
        saut = True
        if self.hauteursaut >= -hauteursaut:
            self.signe = 1
        if self.hauteursaut < 0:
            self.signe = -1
        self.rect.bottom -= int(self.hauteursaut**2 * 0.1 * self.signe)
        self.hauteursaut -= 1
        if self.hauteursaut < -hauteursaut:
            self.hauteursaut = hauteursaut

            saut = False
            if directionsaut == "D":
                self.mouvementsAnimations(1, 1)
            if directionsaut == "G":
                self.mouvementsAnimations(5, 5)
        print(saut)
        return saut


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
