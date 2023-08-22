#################################################################
#
#       Jeu en Pygame pour projet EESI
#       Graphics by Marie
#       Coding by Fred - python 3.8.5
#       ver. alpha-0.1
#
#################################################################
import os


jeuetatinitial = True
leveldemarrage = 0
fenetrelargeur, fenetrehauteur = 800, 600
fenetretaille = (fenetrelargeur, fenetrehauteur)
fenetrecouleur = (4, 9, 46)

scoreinitial = 0
vieoliveinitiale = 5

vitesse = 15
hauteursaut = 12
gravite = 6
entraindesauter = False
policepardefaut = "ttf/PixeloidSans.ttf"
taillepolice = 24

couleurtransparente = (234, 21, 227)

fichierssons = []
for fichier in os.listdir('son/sfx/ogg/') :
    fichierssons.append(os.path.join('son/sfx/ogg/',fichier) )


fichiersmusiques = []
for musique in os.listdir('son/musiques/ogg/'):
    fichiersmusiques.append(os.path.join('son/musiques/ogg/', musique))

fichiersdecors = [
    "img/Map_niveau1_herbe derriere.png",
    "img/Map_niveau1_herbe devant.png",
    "img/Map_niveau1_sol.png",
]


fichiersolive = [
    "img/olive_D1.png",
    "img/olive_D2.png",
    "img/olive_D3.png",
    "img/olive_D2.png",
    "img/olive_G1.png",
    "img/olive_G2.png",
    "img/olive_G3.png",
    "img/olive_G2.png",
    "img/olive_Dsaut.png",
    "img/olive_Gsaut.png",
    "img/olive_marche arriere1.png",
    "img/olive_marche arriere2.png",
    "img/olive_marche arriere3.png",
    "img/olive_marche avant1.png",
    "img/olive_marche avant2.png",
    "img/olive_marche avant3.png",
    "img/olive_face.png",
    "img/olive_armure_D1.png",
    "img/olive_armure_D2.png",
    "img/olive_armure_Dsaut.png",
    "img/olive_armure_G1.png",
    "img/olive_armure_G2.png",
    "img/olive_armure_Dcoup.png",
    "img/olive_armure_Gcoup.png",
    "img/olive_armure_Gsaut.png"
]

fichiersmysteryhuman = [
    "img/MH_1.png",
    "img/MH_2.png",
    "img/MH_3.png",
    "img/MH_anim_bouche ouverte_1.png",
    "img/MH_anim_bouche ouverte_2.png",
    "img/MH_anim_bouche ouverte_3.png",
    "img/MH_anim_bouche ouverte_4.png",
    "img/MH_anim_bouche ouverte_5.png",
    "img/MH_anim_bouche ouverte_6.png",
    "img/MH_anim_bouche ouverte_7.png",
    "img/MH_anim_bouche ouverte_8.png",
    "img/MH_anim_bouche ouverte_9.png",
    "img/MH_anim_bouche ouverte_10.png",
    "img/MH_anim_bouche ouverte_11.png",
    "img/MH_Face.png",
]
fichiersbriques = ["img/brique 1.png", "img/brique 2.png"]
fichiersepee = ["img/jv epee.png"]

estchevalier = False


