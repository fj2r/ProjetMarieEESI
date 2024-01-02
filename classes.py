import pygame as pg
import pygame.sprite
import pygame.freetype

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
            self.listeimagespouranimation.append(img)
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
        self.listesmusiquesL1 = []
        for sfx in fichierssons:
            self.listesfx.append(pg.mixer.Sound(sfx))
        for musique in fichiersmusiquesL1:
            self.listesmusiquesL1.append(pg.mixer.Sound(musique))

    def scrollinggauche(self):
        self.rect.move_ip(-vitesse, 0)

    def scrollingdroite(self):
        self.rect.move_ip(vitesse, 0)

    def scrollinghaut(self, offset):
        self.rect.move_ip(0, +offset)

    def scrollingbas(self, offset):
        self.rect.move_ip(0, +offset)

    def mouvementsAnimations(self, i):
        # print(i)
        self.image = self.listeimagespouranimation[i]
        pg.time.wait(10)

    def mouvementsAnimationsFlip_x(self, i):
        # print(i)
        self.image = self.listeimageflip_x[i]
        pg.time.wait(10)


class Phylactere(Objet):
    """
    : type Objet -> bulle de dialogue des perso
    """

    def __init__(self, image, indexdefaut):
        Objet.__init__(self, image, indexdefaut)
        self.rect.right, self.rect.bottom = 2000 + 69 * 2, fenetrehauteur - 6 - 69 * 2
        self.h, self.w = self.image.get_height(), self.image.get_width()
        # self.texte = "Ceci est un phylactère."
        self.textecouleur = textecouleur
        self.contenanttexte = pg.font.Font(policedialogue, taillepolicedialogues)
        self.policedialogues = pg.freetype.Font(policedialogue, taillepolicedialogues)
        self.urldialogues = urldialogues
        self.listedialogues = recupererdialogue(self.urldialogues)
        self.longueurlistedialogue = len(self.listedialogues)
        self.indexdialogue = 0
        self.calque = pg.Surface(
            (self.w - 30, self.h - 53)
        )  # pour que le fond soit rafraichi en blanc à chaque dialogue
        self.calque.fill((255, 255, 255))

    def update(self) -> None:
        # self.rect.right, self.rect.bottom = positionMH
        # print(self.urldialogues)
        self.listedialogues = recupererdialogue(self.urldialogues)
        self.longueurlistedialogue = len(self.listedialogues)
        if self.indexdialogue <= self.longueurlistedialogue:
            self.image.blit(self.calque, (20, 20))
            self.genererPhylactere()  # on génère le phylactère à chaque update

            # print(self.indexdialogue, "/", self.longueurlistedialogue)

    def genererPhylactere(self):
        """
        génère l'affichage du texte à l'intérieur de la bulle par création d'une somme de mots considérés comme des surfaces
        :return: None
        """
        if self.indexdialogue < self.longueurlistedialogue:
            self.listemots = (
                self.splitdialogueenmots()
            )  # on découpe la phrase en plusieurs mots
            self.space = self.contenanttexte.size(" ")[
                0
            ]  # on calcule la taille d'un espace
            self.posx, self.posy = (30, 20)  # on fixe la position de départ

            for mot in self.listemots:
                self.motsurface = self.contenanttexte.render(
                    mot, True, textecouleur
                )  # pour chaque mot on crée une surface
                (
                    self.wordw,
                    self.wordh,
                ) = (
                    self.motsurface.get_size()
                )  # dont on récupère les tailles par un tuple

                if (
                    self.posx + self.wordw >= self.w - 20
                ):  # on teste si la somme des tailles des surfaces dépasse du cadre
                    self.posx = 20  # on revient au départ sur les x
                    self.posy += self.wordh  # on passe à la ligne suivante
                self.image.blit(
                    self.motsurface, (self.posx, self.posy)
                )  # on n'a plus qu'à afficher dans la bulle
                self.posx += (
                    self.wordw + self.space
                )  # on calcule la position du mot suivant en tenant compte des espaces
            self.posx = 30
            self.posy = 20

    def splitdialogueenmots(self):
        """
        fonction pour récupérer la liste des mots contenus dans chaque dialogue
        """
        if self.indexdialogue <= self.longueurlistedialogue:
            listemots = self.listedialogues[self.indexdialogue].split()
            return listemots


class Boitedialogue(Objet):
    def __init__(self, image, indexdefaut):
        Objet.__init__(self, image, indexdefaut)
        self.rect.centerx, self.rect.centery = (
            fenetrelargeur // 2,
            fenetrehauteur // 2 - 100,
        )
        self.w, self.h = self.image.get_width(), self.image.get_height()
        self.textecouleur = (255, 255, 255)
        self.contenanttexte = pg.font.Font(policedialogue, taillepolicedialogues)
        self.policedialogues = pg.freetype.Font(policedialogue, taillepolicedialogues)
        self.listedialogues = ["Souhaitez-vous aider le Mystery Human (O/N)"]
        self.longueurlistedialogue = len(self.listedialogues)
        self.indexdialogue = 0
        self.calque = pg.Surface(
            (self.w - 10, self.h - 10)
        )  # pour que le fond soit rafraichi en noir à chaque dialogue
        self.calque.fill((0, 0, 0))
        self.reponse = 0

    def update(self):
        # self.image.blit(self.calque, (20, 20))
        self.genererBoite()  # on génère le phylactère à chaque update

    def genererBoite(self):
        self.listemots = (
            self.splitdialogueenmots()
        )  # on découpe la phrase en plusieurs mots
        self.space = self.contenanttexte.size(" ")[
            0
        ]  # on calcule la taille d'un espace
        self.posx, self.posy = (20, self.h // 2)  # on fixe la position de départ

        for mot in self.listemots:
            self.motsurface = self.contenanttexte.render(
                mot, True, (255, 255, 0)
            )  # pour chaque mot on crée une surface
            (
                self.wordw,
                self.wordh,
            ) = self.motsurface.get_size()  # dont on récupère les tailles par un tuple

            if (
                self.posx + self.wordw >= self.w - 20
            ):  # on teste si la somme des tailles des surfaces dépasse du cadre
                self.posx = 20  # on revient au départ sur les x
                self.posy += self.wordh  # on passe à la ligne suivante
            self.image.blit(
                self.motsurface, (self.posx, self.posy)
            )  # on n'a plus qu'à afficher dans la bulle
            self.posx += (
                self.wordw + self.space
            )  # on calcule la position du mot suivant en tenant compte des espaces
        self.posx = 20
        self.posy = self.h // 2

    def splitdialogueenmots(self):
        """
        fonction pour récupérer la liste des mots contenus dans chaque dialogue
        """
        listemots = self.listedialogues[self.indexdialogue].split()
        return listemots


class Olive(Objet):
    """
    : type Objet
    :arg Vecteur avec les fichiers pour afficher les animations du sprite
    """

    def __init__(self, image, indexdefaut):
        Objet.__init__(self, image, indexdefaut)
        self.level = 1
        self.rect.y = 200
        self.offset = 0
        self.rect.left = (fenetrelargeur - self.rect.w) // 20
        self.hauteursaut = hauteursaut
        self.direction = "D"
        self.entraindesauter = False
        self.entraindesauterL2 = False
        self.entraindetomber = False
        self.entraindetomberL2 = False
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
        self.decory = fenetrehauteur
        self.decorx = 0

    def gravite(self, gravite):
        self.rect.y += gravite

    def graviteL2(self, gravite):

        self.rect.y += 0
        if self.decory <= fenetrehauteur:
            self.decory += gravite // 4
        else:
            self.decory += 0

    def update(
        self,
        listesolsprites,
        listebriquessprites,
        listeepeesprites,
        zonescoreetvie,
        listeoeilsprites,
        listemysterysprites,
        sol,
    ):

        ##################################################
        #           Liste des tests de collisions
        #################################################
        listecollisionoliveoeil = pg.sprite.spritecollide(self, listeoeilsprites, True)
        listecollisionsolivesbriques = pg.sprite.spritecollide(
            self, listebriquessprites, False
        )

        listecollisionsoliveepee = pg.sprite.spritecollide(self, listeepeesprites, True)
        listecollisionsolivesol = pg.sprite.spritecollide(self, listesolsprites, False)
        listecollisionolivemysteryhuman = pg.sprite.spritecollide(
            self, listemysterysprites, False
        )

        ##################################################"
        if listecollisionoliveoeil:
            # print("le doigt dans l'oeil !")
            self.listesfx[0].play(0, 0, 0)
            zonescoreetvie.calculScore(5)
        if listecollisionsoliveepee:
            # print("voila il a l'épée !")
            self.estchevalier = True
            self.listesfx[0].play(0, 0, 0)
            zonescoreetvie.calculScore(20)
            self.index = 0
        if listecollisionolivemysteryhuman:
            # print("Enfin le voilà !")
            pass

        if listecollisionsolivesbriques:
            self.cstgravitaire = 0
            for brique in listecollisionsolivesbriques:
                print("je suis sur une brique")
                self.rect.bottom = brique.rect.top + 1
                self.decory += 0
                self.sautinterrompu = True
                self.cstgravitaire = 0

        elif listecollisionsolivesol:

            for sol in listecollisionsolivesol:
                self.rect.bottom = sol.rect.y + 1

                self.decory += 0

            self.cstgravitaire = 0
            # self.entraindesauter = False
            # self.entraindetomber = False

        else:
            self.cstgravitaire = gravite

        # gestion des mouvements de sauts
        if self.entraindesauter == True:

            if self.estchevalier == False:
                self.sauter(hauteursaut, self.framesautolive)
            else:
                self.sauter(hauteursaut, self.framesautchevalier)

        if self.entraindesauterL2 == True:

            if self.estchevalier == False:
                self.sauterL2(hauteursaut, self.framesautolive, sol)

            else:
                self.sauterL2(hauteursaut, self.framesautchevalier, sol)
        if self.level == 1:
            self.gravite(self.cstgravitaire)
        if self.level == 2:
            self.gravite(self.cstgravitaire)

            self.graviteL2(self.cstgravitaire)

        """if self.entraindesauterL2 == False:
            if self.rect.bottom >= fenetrehauteur - 6 :
                self.rect.move_ip(0, 0)
                self.decory -= gravite
            else:
                self.rect.move_ip(0, gravite)
                self.decory += gravite"""

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

    def deplacerGaucheL2(self, listeframes):
        self.mouvementsAnimationsFlip_x(listeframes[self.index])
        self.index += 1
        self.index = self.index % len(listeframes)
        if self.rect.left < 0:
            self.rect.move_ip(0, 0)
        else:
            self.rect.move_ip(-vitesse, 0)
        self.direction = "G"
        return "G"

    def deplacerDroite(self, listeframes):
        self.mouvementsAnimations(listeframes[self.index])
        self.index += 1
        self.index = self.index % len(listeframes)

        if self.rect.x < (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(vitesse, 0)
        if self.rect.x >= (fenetrelargeur - self.rect.w) // 2:
            self.rect.move_ip(0, 0)
        self.direction = "D"

        return "D"

    def deplacerDroiteL2(self, listeframes):
        self.mouvementsAnimations(listeframes[self.index])
        self.index += 1
        self.index = self.index % len(listeframes)
        if self.rect.right > fenetrelargeur:
            self.rect.move_ip(0, 0)
        else:
            self.rect.move_ip(+vitesse, 0)
        self.direction = "D"
        return "D"

    def sauter(self, hauteursautmax, listeframes):
        self.signe = +1
        self.offset = 0
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

    def sauterL2(self, hauteursautmax, listeframes, sol):
        self.signe = +1
        self.offset = 0
        if self.entraindesauterL2 == True:

            if self.direction == "D":
                self.mouvementsAnimations(listeframes[0])
            if self.direction == "G":
                self.mouvementsAnimationsFlip_x(listeframes[0])

            self.offset = int(self.hauteursaut**2 * (1 / 2) * self.signe)

            self.rect.y -= self.offset
            self.decory -= self.offset

            self.hauteursaut -= 1
            if self.hauteursaut < 0:
                self.signe = -1
                self.entraindetomber = True
                self.entraindesauterL2 = False
                self.decory += self.offset
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
        # self.hauteursaut = hauteursautmax


class Mysteryhuman(Objet):
    def __init__(self, image, indexdefaut):
        Objet.__init__(self, image, indexdefaut)
        self.rect.left, self.rect.bottom = 2000, fenetrehauteur - 6
        self.vies = 1
        self.dommages = 1
        self.sequence = 0
        self.index = 0
        self.listeframesselever = [2, 4, 2, 4, 5, 7]
        self.index2 = 0
        self.listeframesparler = [10, 13, 14, 14, 13, 10]
        self.indexdialogue = 0

        self.listeframesavaler = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        self.index3 = 0

        self.reponse = 0
        self.findesequence = 0

    def update(
        self,
        listeboitedialogue,
        listeolivesprite,
        listebullesprite,
        positionMH,
        fenetre,
        boitedialogue,
        bulle,
    ):

        listecollisionmysteryhumanolive = pg.sprite.spritecollide(
            self, listeolivesprite, False
        )
        if listecollisionmysteryhumanolive:

            if self.sequence == 0:  # animation du perso qui se lève
                if self.index < len(self.listeframesselever):
                    self.selever()
                else:
                    self.listesmusiquesL1[0].fadeout(100)
                    self.sequence = 1

            if self.sequence == 1:  # animation pour 1ère partie dialogue

                if bulle.indexdialogue < bulle.longueurlistedialogue:

                    if self.index2 < len(self.listeframesparler):
                        self.parler()

                        listebullesprite.draw(
                            fenetre
                        )  # affichage des sprites de bulles

                else:
                    self.listesfx[2].fadeout(100)
                    self.index2 = 0
                    bulle.indexdialogue = 0
                    self.sequence = 2

            if self.sequence == 2:  # question dans la boite de dialogue
                if self.reponse == 0:
                    listeboitedialogue.draw(fenetre)
                if self.reponse == 1:
                    self.sequence = 3
                if self.reponse == 2:
                    self.sequence = 4
                else:
                    self.reponse = 0

            if self.sequence == 3:  # si réponse oui -> dialogue continue
                bulle.urldialogues = urldialoguesOUI
                if bulle.indexdialogue < bulle.longueurlistedialogue:
                    # print(bulle.indexdialogue, "/", bulle.longueurlistedialogue)
                    if self.index2 < len(self.listeframesparler):
                        self.parler()

                        listebullesprite.draw(
                            fenetre
                        )  # affichage des sprites de bulles
                else:
                    self.index2 = 0
                    self.sequence = 5
            if self.sequence == 4:  # si réponse non

                bulle.urldialogues = urldialoguesNON
                if bulle.indexdialogue < bulle.longueurlistedialogue:
                    self.affichePortrait(fenetre)
                    # print(bulle.indexdialogue, "/", bulle.longueurlistedialogue)
                    if self.index2 < len(self.listeframesparler):
                        self.parler()

                        listebullesprite.draw(
                            fenetre
                        )  # affichage des sprites de bulles
                else:
                    self.effacerPortrait(fenetre)
            if self.sequence == 5:
                zonescoreetvie.calculScore(50)
                self.fin = self.avalerOlive()
                if self.fin == True:
                    self.sequence = 6
                pg.time.wait(500)
            if self.sequence == 6:
                self.findesequence = 1
                listeolivesprite.rect.x = 200
                listeolivesprite.rect.y = 200

        else:
            self.listesmusiquesL1[0].stop()
            self.listesfx[2].stop()

    def animation(self):
        pass

    def selever(self):
        self.listesmusiquesL1[0].play(0, 0, 0)
        self.mouvementsAnimations(self.listeframesselever[self.index])
        # self.rect.left, self.rect.bottom = 2000, fenetrehauteur - 50
        self.index += 1

        pg.time.wait(300)
        self.listesmusiquesL1[0].stop()

    def parler(self):
        self.listesfx[2].play(0, 0, 10)
        self.mouvementsAnimations(self.listeframesparler[self.index2])
        # self.rect.left, self.rect.bottom = 2000, fenetrehauteur - 50
        self.index2 += 1
        self.index2 = self.index2 % len(self.listeframesparler)

        pg.time.wait(200)
        self.listesfx[2].stop()

    def avalerOlive(self):  # retourne un booléen quand la fonction est terminée
        self.mouvementsAnimations(self.listeframesavaler[self.index3])
        self.index3 += 1
        self.index3 = self.index3 % len(self.listeframesavaler)
        pg.time.wait(200)
        if self.index3 == 0:
            return True
        else:
            return False

    def affichePortrait(self, fenetre):
        self.urlportrait = urlportrait[0]
        # print(self.urlportrait)
        self.portrait = pygame.image.load(self.urlportrait).convert_alpha()
        self.portrait.set_colorkey(couleurtransparente)
        self.portrait = pg.transform.scale2x(self.portrait)
        self.rectportrait = self.portrait.get_rect()
        self.rectportrait.h, self.rectportrait.w = (
            self.portrait.get_height(),
            self.portrait.get_width(),
        )
        self.rectportrait.centerx, self.rectportrait.centery = (
            fenetrelargeur // 2,
            fenetrehauteur // 2 - 100,
        )

        fenetre.blit(self.portrait, (fenetrelargeur // 2 - self.rectportrait.x, 0))

    def effacerPortrait(self, fenetre):
        self.portrait.fill(fenetrecouleur)
        print("calque")

    def genererdialogues(self, index):
        blabla = recupererdialogue(urldialogues)
        # print(blabla)

    def attaque(self):
        pass

    def dialogue(self):
        pass

    def scrollinghaut(self):
        self.rect.move_ip(0, -vitesse)

    def scrollingbas(self):
        self.rect.move_ip(0, vitesse)


class Epee(Objet):
    def __init__(self, images, indexdefaut):
        Objet.__init__(self, images, indexdefaut)
        self.rect.centerx = epee_centerx
        self.rect.y = epee_y

    def scrollinggauche(self):
        self.rect.move_ip(-vitesse, 0)

    def scrollingdroite(self):
        self.rect.move_ip(vitesse, 0)

    def scrollinghaut(self, offset):
        self.rect.move_ip(0, -offset)

    def scrollingbas(self, offset):
        self.rect.move_ip(0, +offset)


class Porte(Objet):
    def __init__(self, images, indexdefaut):
        Objet.__init__(self, images, indexdefaut)
        self.rect.left = 3000
        self.rect.bottom = fenetrehauteur - 6

    def update(self):
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

    def update(self):
        pass

    def scrollinggauche(self):
        self.rect.move_ip(-vitesse, 0)

    def scrollingdroite(self):
        self.rect.move_ip(vitesse, 0)

    def scrollinghaut(self, offset):
        self.rect.move_ip(0, +offset)

    def scrollingbas(self, offset):
        self.rect.move_ip(0, +offset)


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
