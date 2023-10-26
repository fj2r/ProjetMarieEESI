import pygame as pg
import pygame.sprite

from config import *


class Objet(pygame.sprite.Sprite):
    """Classe parent qui hérite de la classe
    Sprite.
    Sert à instancier des objets de type Rect.
    :return None"""

    def __init__(self, image, indexdefaut):
        pygame.sprite.Sprite.__init__(self)
        self.listeimagespouranimation = []
        self.listeimageflip_x = []
        self.index = 0
        for element in image:
            img = pygame.image.load(element).convert_alpha()
            img.set_colorkey(couleurtransparente)
            img = pg.transform.scale2x(img)
            self.listeimagespouranimation.append(
                img
            )
            self.listeimageflip_x.append(pg.transform.flip(img, True, False))

        self.image = self.listeimagespouranimation[indexdefaut]
        """self.image.set_colorkey(couleurtransparente)
        self.image = pg.transform.scale2x(self.image)"""

        self.rect = self.image.get_rect()
        self.rect.h = self.image.get_height()
        self.rect.w = self.image.get_width()
        self.timer = 0
        self.cstgravitaire = gravite
        self.listesfx = []
        for sfx in fichierssons:
            self.listesfx.append(pg.mixer.Sound(sfx))


class Phylactere(Objet):
    """
    : type Objet -> bulle de dialogue des perso
    """

    def __init__(self, image, indexdefaut):
        Objet.__init__(self, image, indexdefaut)
        self.rect.y = 100
        self.rect.x = 300
        self.rect.size = (500, 500)
        self.texte = "Ceci est un phylactère."
        self.contenanttexte = pg.font.Font(policepardefaut, 14)

    def update(self) -> None:
        pass
    def genererPhylactere(self, phylactere):
        pass

    def texte(self, fenetre):

        self.textefinal = self.contenanttexte.render("%s" % self.texte, 0, (255, 255, 255))

        fenetre.blit(self.textefinal, (20, 20))


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
        self.index = 0
        self.animation_timer = 0.1
        self.current_frame = 0
        self.framesautolive = [4]
        self.framesautchevalier = [19]

    def gravite(self, gravite):
        self.rect.y += gravite
        print(gravite)

    def update(
        self,
            listesolsprites,
            listebriquessprites,
            listeepeesprites,
            listeportesprites,
            zonescoreetvie,
            listeoeilsprites
    ):
        ##################################################
        #           Liste des tests de collisions
        #################################################
        listecollisionoliveoeil = pg.sprite.spritecollide(self, listeoeilsprites, True)
        listecollisionsolivesbriques = pg.sprite.spritecollide(
            self, listebriquessprites, False
        )
        listecollisionsoliveporte = pg.sprite.spritecollide(self, listeportesprites, False)
        listecollisionsoliveepee = pg.sprite.spritecollide(self, listeepeesprites, True)
        listecollisionsolivesol = pg.sprite.spritecollide(self, listesolsprites, False)
        ##################################################"
        if listecollisionoliveoeil :
            print("le doigt dans l'oeil !")
            self.listesfx[0].play(0, 0, 0)
            zonescoreetvie.calculScore(5)

        if listecollisionsoliveporte :
            print("Aïe la porte !")
        if listecollisionsolivesbriques:
            #print("collision brique")
            for brique in listecollisionsolivesbriques:

                self.rect.bottom = brique.rect.y + 0
                self.sautinterrompu = True

            self.cstgravitaire = 0

        else:
            self.cstgravitaire = gravite

        if listecollisionsolivesol:
            #print("collision sol")
            for sol in listecollisionsolivesol:
                self.rect.bottom = sol.rect.y + 1

            self.cstgravitaire = 0
            # self.entraindesauter = False
            # self.entraindetomber = False
        else:
            self.cstgravitaire = gravite

        if self.entraindesauter == True:
            if self.estchevalier == False :
                self.sauter(hauteursaut, self.framesautolive)
            else :
                self.sauter(hauteursaut, self.framesautchevalier)

        self.gravite(self.cstgravitaire)
        #print(self.cstgravitaire)

        if listecollisionsoliveepee:
            print("voila il a l'épée !")
            self.estchevalier = True
            self.listesfx[0].play(0, 0, 0)
            zonescoreetvie.calculScore(20)
            self.index=0

    def deplacerGauche(self, listeframes):

        self.mouvementsAnimationsFlip_x(listeframes[self.index])
        self.index += 1
        self.index = self.index % len(listeframes)

        if self.rect.x == 0:
            self.rect.move_ip(0, 0)
        if self.rect.x < (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(-vitesse, 0)
        if self.rect.x >= (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(0, 0)
        self.direction = "G"
        return "G"
    def deplacerGaucheL2(self,listeframes):
        self.mouvementsAnimationsFlip_x(listeframes[self.index])
        self.index += 1
        self.index = self.index % len(listeframes)
        if self.rect.left < 0  :
            self.rect.move_ip(0,0)
        else :
            self.rect.move_ip(-vitesse,0)

    def deplacerDroite(self, listeframes):

        self.mouvementsAnimations(listeframes[self.index])
        self.index +=1
        self.index = self.index % len(listeframes)

        if self.rect.x < (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(vitesse, 0)
        if self.rect.x >= (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(0, 0)
        self.direction = "D"
        return "D"
    def deplacerDroiteL2(self,listeframes):
        self.mouvementsAnimations(listeframes[self.index])
        self.index += 1
        self.index = self.index % len(listeframes)
        if self.rect.right > fenetrelargeur :
            self.rect.move_ip(0,0)
        else :
            self.rect.move_ip(+vitesse,0)
    def mouvementsAnimations(self, i):
        print(i)
        self.image = self.listeimagespouranimation[i]
        pg.time.wait(0)
    def mouvementsAnimationsFlip_x(self, i):
        print(i)
        self.image = self.listeimageflip_x[i]
        pg.time.wait(0)
    def sauter(self, hauteursautmax, listeframes):

        if self.entraindesauter == True:
            if self.direction == "D":
                self.mouvementsAnimations(listeframes[0])
            if self.direction == "G":
                self.mouvementsAnimationsFlip_x(listeframes[0])
            self.offset = int(self.hauteursaut**2 * (1 / 2) * self.signe)
            self.rect.y -= self.offset
            self.hauteursaut -= 1
            if self.hauteursaut < 0:
                self.signe = -1
                self.entraindetomber = True
            if self.hauteursaut == -hauteursautmax - 1:
                self.entraindesauter = False
                self.entraindetomber = False
                self.signe = 1
                self.hauteursaut = hauteursautmax
        if self.sautinterrompu == True and self.entraindetomber == True:
            self.entraindesauter = False
            self.entraindetomber = False
            self.offset = 0
            self.signe = 1
            self.hauteursaut = hauteursautmax


class Mysteryhuman(Objet):
    def __init__(self, image, indexdefaut):
        Objet.__init__(self, image, indexdefaut)
        self.rect.x, self.rect.y = 2000, 400
        self.vies = 1
        self.dommages = 1
    def update(self):
        pass
    def animation(self):
        pass
    def attaque(self):
        pass
    def dialogue(self):
        pass


class Epee(Objet):
    def __init__(self, images, indexdefaut):
        Objet.__init__(self, images, indexdefaut)
        self.rect.left = 2000
        self.rect.bottom = fenetrehauteur - 6

    def scrollinggauche(self):
        self.rect.move_ip(-vitesse, 0)

    def scrollingdroite(self):
        self.rect.move_ip(vitesse, 0)

class Porte(Objet):
    def __init__(self, images, indexdefaut):
        Objet.__init__(self, images, indexdefaut)
        self.rect.left = 3000
        self.rect.bottom = fenetrehauteur - 6

    def update(self) :
        pass
    def scrollinggauche(self):
        self.rect.move_ip(-vitesse, 0)

    def scrollingdroite(self):
        self.rect.move_ip(vitesse, 0)

class Oeil(Objet):
    def __init__(self, images, indexdefaut):
        Objet.__init__(self, images, indexdefaut)
        self.rect.x = 0
        self.rect.y = 0
        self.points = 5


    def update(self) :
        pass
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
