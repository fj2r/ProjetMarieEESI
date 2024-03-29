#################################################################
#
#       Jeu en Pygame pour projet EESI
#       Graphics by Marie
#       Coding by Fred - python 3.8.5
#       ver. beta-0.6
#
#################################################################
from fonctions import *
from fonctions import remplissageImagesSonsJeu, calculListePositionObjets

jeuetatinitial = True
leveldemarrage = 0
fenetrelargeur, fenetrehauteur = 960, 660
fenetretaille = (fenetrelargeur, fenetrehauteur)
fenetrecouleur = (4, 9, 46)

scoreinitial = 0
vieoliveinitiale = 6
estchevalier = False
timer = 0.01  # réglage du délai entre deux frames

vitesse = 10
hauteursaut = 12
gravite = 6
entraindesauter = False


couleurtransparente = (234, 21, 227)

#############################################################
# Sons du jeu
#############################################################
fichierssons = remplissageImagesSonsJeu("son/sfx/ogg/")
fichiersmusiquesL1 = remplissageImagesSonsJeu("son/musiques/ogg/")
#############################################################
# éléments de design des décors
#############################################################
fichiersdecors = [
    "img/Map_niveau1_herbe derriere.png",
    "img/Map_niveau1_herbe devant.png",
    "img/Map_niveau1_sol.png",
]
fichiersmapsecrete = remplissageImagesSonsJeu("img/map_secrète/")
fichiersbriques = ["img/items/brique 1.png", "img/items/brique 2.png"]
#############################################################
# éléments de design des items
#############################################################
fichiersitems = remplissageImagesSonsJeu("img/items/")
fichiersoeil = ["img/items/oeil_a_collecter.png"]
fichiersportedefin = remplissageImagesSonsJeu("img/porte de fin/")
fichiersepee = ["img/items/jv epee.png"]
fichiersballes = ["img/items/zattaque_lumière.png"]
#############################################################
# éléments de design des personnages
#############################################################
fichiersbulles = remplissageImagesSonsJeu("img/bulles/")


fichiersolive = remplissageImagesSonsJeu("img/olive deplacements/")
fichiersolivechevalier = remplissageImagesSonsJeu("img/olive_deplacemnts_armure/")
fichiersoliveconcatenee = fichiersolive + fichiersolivechevalier

fichiersmysteryhuman = remplissageImagesSonsJeu("img/perso mystère/")
fichiersmysteryhumancombat = remplissageImagesSonsJeu("img/mystery_human_combat/")
fichierspoeme = ["img/map_secrète/poème_secret.png"]
urlportrait = ["img/perso mystère/MH_Face.png"]
urlfindujeu = ["img/olive_trouve_épée_image entière.png"]
##############################################################
#               Configuration du nombre d'items et positions
##############################################################
# MH en mode combat :
MHcombat_x, MHcombat_y = fenetrelargeur - 100, fenetrehauteur-27500
# Epee :
epee_centerx = 2700
epee_y = fenetrehauteur - 5000

# Les briques :
nbbriques = 120
taillebrique = 60
listepositionbriques = calculListePositionBriquesL2(
    nbbriques, taillebrique, fenetrelargeur, fenetrehauteur,MHcombat_x, MHcombat_y
)


# les yeux :
# positionoeil = [(500, 200), (800, 200), (1200, 200)]
nboeil = 30
tailloeil = 64

listepositionyeux = calculListePositionYeuxL2(
    nboeil, tailloeil, fenetrelargeur, fenetrehauteur
)

##############################################################
#              dialogues des personnages
##############################################################
fichierboitedialogue = ["img/bulles/bulle_informatons.png"]
urldialogues = "dial/dialoguesMH.txt"
urldialoguesOUI = "dial/dialoguesMHOUI.txt"
urldialoguesNON = "dial/dialoguesMHNON.txt"
urldialoguesCombat1 = "dial/dialoguesMHcombat1.txt"
urldialoguesCombat2= "dial/dialoguesMHcombat2.txt"
urlpoeme = "dial/poeme.txt"

policedialogue = "ttf/PixeloidSans.ttf"
taillepolicedialogues = 14
textecouleur = (0, 0, 0)
##############################################################
#              textes hors dialogues (splash, barre de statuts...)
##############################################################
policepardefaut = "ttf/PixeloidSans.ttf"
taillepolice = 24
