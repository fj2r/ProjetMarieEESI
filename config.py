#################################################################
#
#       Jeu en Pygame pour projet EESI
#       Graphics by Marie
#       Coding by Fred - python 3.8.5
#       ver. alpha-0.1
#
#################################################################
from fonctions import *
from fonctions import remplissageImagesSonsJeu

jeuetatinitial = True
leveldemarrage = 0
fenetrelargeur, fenetrehauteur = 960, 660
fenetretaille = (fenetrelargeur, fenetrehauteur)
fenetrecouleur = (4, 9, 46)

scoreinitial = 0
vieoliveinitiale = 5
estchevalier = False
timer = 0.01 #réglage du délai entre deux frames

vitesse = 10
hauteursaut = 12
gravite = 8
entraindesauter = False
policepardefaut = "ttf/PixeloidSans.ttf"
taillepolice = 24

couleurtransparente = (234, 21, 227)

#############################################################
# Sons du jeu
#############################################################
fichierssons = remplissageImagesSonsJeu("son/sfx/ogg/")

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
#############################################################
# éléments de design des personnages
#############################################################
fichiersbulles = remplissageImagesSonsJeu("img/bulles/")


fichiersolive = remplissageImagesSonsJeu("img/olive deplacements/")
fichiersolivechevalier = remplissageImagesSonsJeu('img/olive_deplacemnts_armure/')
fichiersoliveconcatenee = fichiersolive + fichiersolivechevalier

fichiersmysteryhuman = remplissageImagesSonsJeu("img/perso mystère/")
fichiersmysteryhumancombat = remplissageImagesSonsJeu('img/mystery_human_combat/')

##############################################################
#               Configuration du nombre d'items et positions
##############################################################

# Les briques :
nbbrique = 20
taillebrique = 60
listepositionbriques  = []
for i in range (0,nbbrique):
    positionbrique = (100+taillebrique*2*i,300)
    listepositionbriques.append(positionbrique)

# les yeux :
positionoeil = [(500,200),(800,200),(1200,200)]
nboeil = len(positionoeil)

# Les