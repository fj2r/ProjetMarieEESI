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

    def scrollinghaut(self):
        self.rect.move_ip(0, -vitesse)

    def scrollingbas(self):
        self.rect.move_ip(0, vitesse)

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
        self.rect.right, self.rect.bottom = 2000+69*2, fenetrehauteur - 6 - 69*2
        self.h, self.w = self.image.get_height(), self.image.get_width()
        self.texte = "Ceci est un phylactère."
        self.textecouleur = textecouleur
        self.contenanttexte = pg.font.Font(policedialogue, taillepolicedialogues)
        self.policedialogues = pg.freetype.Font(policedialogue, taillepolicedialogues)
        self.listedialogues = recupererdialogue(urldialogues)
        self.indexdialogue = 0

    def update(self, fenetre, positionMH) -> None:
        #self.rect.right, self.rect.bottom = positionMH
        self.genererPhylactere() # on génère le phylactère à chaque update

    def genererPhylactere(self):
        '''
        génère l'affichage du texte à l'intérieur de la bulle par création d'une somme de mots considérés comme des surfaces
        :return: None
        '''
        self.listemots = self.splitdialogueenmots() #on découpe la phrase en plusieurs mots
        self.space = self.contenanttexte.size(' ')[0] # on calcule la taille d'un espace
        self.posx, self.posy = (20,20) # on fixe la position de départ

        for mot in self.listemots :
            self.motsurface = self.contenanttexte.render(mot, True, textecouleur) #pour chaque mot on crée une surface
            self.wordw, self.wordh = self.motsurface.get_size() # dont on récupère les tailles par un tuple

            if self.posx + self.wordw >= self.w : #on teste si la somme des tailles des surfaces dépasse du cadre
                self.posx = 20 #on revient au départ sur les x
                self.posy += self.wordh #on passe à la ligne suivante
            self.image.blit(self.motsurface, (self.posx,self.posy)) # on n'a plus qu'à afficher dans la bulle
            self.posx += self.wordw + self.space #on calcule la position du mot suivant en tenant compte des espaces
        self.posx = 20
        self.posy = 20
        ''' self.textecourant = self.contenanttexte.render(
            "%s" % self.listedialogues[self.indexdialogue], True, textecouleur
        )
        #self.image.blit(self.currenttext,(20,20))
        self.image.blit(self.textecourant, (20, 20))'''



    def splitdialogueenmots(self):
        '''
        fonction pour récupérer la liste des mots contenus dans chaque dialogue

        '''
        listemots = (self.listedialogues[self.indexdialogue].split())
        return listemots

class Olive(Objet):
    """
    : type Objet
    :arg Vecteur avec les fichiers pour afficher les animations du sprite
    """

    def __init__(self, image, indexdefaut):
        Objet.__init__(self, image, indexdefaut)
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
        self.decory -= gravite
        # print(self.decory)

    def update(
        self,
        listesolsprites,
        listebriquessprites,
        listeepeesprites,
        zonescoreetvie,
        listeoeilsprites,
        listemysterysprites,
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
            print("le doigt dans l'oeil !")
            self.listesfx[0].play(0, 0, 0)
            zonescoreetvie.calculScore(5)
        if listecollisionsoliveepee:
            print("voila il a l'épée !")
            self.estchevalier = True
            self.listesfx[0].play(0, 0, 0)
            zonescoreetvie.calculScore(20)
            self.index = 0
        if listecollisionolivemysteryhuman:
            print("Enfin le voilà !")
            zonescoreetvie.calculScore(50)

        if listecollisionsolivesbriques:
            # print("collision brique")
            for brique in listecollisionsolivesbriques:

                self.rect.bottom = brique.rect.y + 0
                self.sautinterrompu = True

            self.cstgravitaire = 0

        else:
            self.cstgravitaire = gravite

        if listecollisionsolivesol:
            # print("collision sol")
            for sol in listecollisionsolivesol:
                self.rect.bottom = sol.rect.y + 1

            self.cstgravitaire = 0
            # self.entraindesauter = False
            # self.entraindetomber = False
        else:
            self.cstgravitaire = gravite

        # gestion des mouvements de sauts
        if self.entraindesauter == True:
            print("hop !")
            if self.estchevalier == False:
                self.sauter(hauteursaut, self.framesautolive)
            else:
                self.sauter(hauteursaut, self.framesautchevalier)
        self.gravite(self.cstgravitaire)

        if self.entraindesauterL2 == True:
            if self.estchevalier == False:
                self.sauterL2(hauteursaut, self.framesautolive)

            else:
                self.sauterL2(hauteursaut, self.framesautchevalier)
        self.graviteL2(self.cstgravitaire)

        # print(self.cstgravitaire)

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

    def sauterL2(self, hauteursautmax, listeframes):
        if self.entraindesauterL2 == True:
            if self.direction == "D":
                self.mouvementsAnimations(listeframes[0])
            if self.direction == "G":
                self.mouvementsAnimationsFlip_x(listeframes[0])
            self.offset = int(self.hauteursaut**2 * (1 / 2) * self.signe)
            self.decory -= self.offset
            self.hauteursaut -= 1
            if self.hauteursaut < 0:
                self.signe = -1
                self.entraindetomberL2 = True
            if self.hauteursaut == -hauteursautmax - 1:
                self.entraindesauterL2 = False
                self.entraindetomberL2 = False
                self.signe = 1
                self.hauteursaut = hauteursautmax
        if self.sautinterrompu == True and self.entraindetomberL2 == True:
            self.entraindesauterL2 = False
            self.entraindetomberL2 = False
            self.offset = 0
            self.signe = 1
            self.hauteursaut = hauteursautmax
        if self.entraindesauterL2 == False:
            self.decory += gravite


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

    def update(self, listeolivesprite, listebullesprite,positionMH, fenetre):
        listecollisionmysteryhumanolive = pg.sprite.spritecollide(
            self, listeolivesprite, False
        )
        if listecollisionmysteryhumanolive:

            if self.sequence == 0:
                if self.index < len(self.listeframesselever):
                    self.selever()
                else:
                    self.listesmusiquesL1[0].fadeout(100)
                    self.sequence = 1

            if self.sequence == 1:

                if self.index2 < len(self.listeframesparler):
                    self.parler()

                    listebullesprite.draw(fenetre)

                else:
                    self.listesfx[2].fadeout(100)
                    self.sequence = 2

            if self.sequence == 2:
                pass

        else :
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

    def parler(self):
        self.listesfx[2].play(0, 0, 0)
        self.mouvementsAnimations(self.listeframesparler[self.index2])
        # self.rect.left, self.rect.bottom = 2000, fenetrehauteur - 50
        self.index2 += 1
        self.index2 = self.index2 % len(self.listeframesparler)

        pg.time.wait(100)

    def genererdialogues(self, index):
        blabla = recupererdialogue(urldialogues)
        print(blabla)

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
        self.rect.left = 1000
        self.rect.bottom = fenetrehauteur - 6

    def scrollinggauche(self):
        self.rect.move_ip(-vitesse, 0)

    def scrollingdroite(self):
        self.rect.move_ip(vitesse, 0)

    def scrollinghaut(self):
        self.rect.move_ip(0, -vitesse)

    def scrollingbas(self):
        self.rect.move_ip(0, vitesse)


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

    def scrollinghaut(self):
        self.rect.move_ip(0, -vitesse)

    def scrollingbas(self):
        self.rect.move_ip(0, vitesse)


class Sol(Objet):
    def __init__(self, image, indexdefaut):
        Objet.__init__(self, image, indexdefaut)
        self.rect.left = 0
        self.rect.y = fenetrehauteur - 20

    def scrollinggauche(self):
        self.rect.move_ip(-vitesse, 0)

    def scrollingdroite(self):
        self.rect.move_ip(vitesse, 0)

    def scrollingverticalhaut(self):
        self.rect.move_ip(0, -vitesse)

    def scrollingverticalbas(self):
        self.rect.move_ip(0, +vitesse)


class Brique(Objet):
    def __init__(self, image, indexdefaut):
        Objet.__init__(self, image, indexdefaut)
        self.rect.bottom = (fenetrehauteur // 2) + 50
        self.rect.right = fenetrelargeur

    def scrollinggauche(self):
        self.rect.move_ip(-vitesse, 0)

    def scrollingdroite(self):
        self.rect.move_ip(vitesse, 0)

    def scrollinghaut(self):
        self.rect.move_ip(0, -vitesse)

    def scrollingbas(self):
        self.rect.move_ip(0, vitesse)


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
