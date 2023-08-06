import pygame as pg
import pygame.sprite

from conf import *


class Objet(pygame.sprite.Sprite):
    '''Classe parent qui hérite de la classe
    Sprite.
    Sert à instancier des objets de type Rect.
    :return None'''

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.listeimagespouranimation = []
        self.index = 0
        for element in image:
            self.listeimagespouranimation.append(pygame.image.load(element).convert_alpha())

        self.image = self.listeimagespouranimation[14]
        self.image.set_colorkey(couleurtransparente)
        self.image = pg.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        self.rect = self.image.get_rect()
        self.rect.h = self.image.get_height()
        self.rect.w = self.image.get_width()
        self.timer = 0


class Olive(Objet):
    '''
    :type Objet
    :arg Vecteur avec les fichiers pour afficher les animations du sprite
     '''

    def __init__(self, image):
        Objet.__init__(self, image)

        self.rect.bottom = fenetrehauteur
        self.rect.left = (fenetrelargeur - self.rect.w) // 10
        self.hauteursaut = hauteursaut
        self.entraindesauter = False
        self.iterateur = 0

    def deplacerGauche(self, indexdepart, indexarret):
        self.framedelai = self.timer
        if self.framedelai <= 0:
            self.mouvementsAnimations(indexdepart, indexarret)
        self.timer -= 1
        if self.rect.x < (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(-vitesse, 0)
        if self.rect.x >= (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(0, 0)
        return 'G'

    def deplacerDroite(self, indexdepart, indexarret):
        self.framedelai = self.timer
        if self.framedelai <= 0:
            self.mouvementsAnimations(indexdepart, indexarret)

        if self.rect.x < (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(vitesse, 0)
        if self.rect.x >= (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(0, 0)

        return 'D'

    def mouvementsAnimations(self, indexdepart, indexarret):
        self.index = indexdepart + self.iterateur
        self.arretindex = indexarret

        # print(self.index)
        if self.index >= self.arretindex:
            self.iterateur = 0
            self.index = indexdepart
        self.image = self.listeimagespouranimation[self.index]
        self.image.set_colorkey(couleurtransparente)
        self.image = pg.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))

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
        self.rect.bottom -= int(self.hauteursaut ** 2 * 0.1 * self.signe)
        self.hauteursaut -= 1
        if self.hauteursaut < -hauteursaut:
            self.hauteursaut = hauteursaut

            saut = False
            if directionsaut == 'D':
                self.mouvementsAnimations(1, 1)
            if directionsaut == 'G':
                self.mouvementsAnimations(5, 5)
        print(saut)
        return saut
