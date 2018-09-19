from Classes import Joueur,Monstre
from CHEST import Fenetre
from tkinter import PhotoImage
from os import listdir

version="1 . 2 . 2"

police1_10=("Cracked Code",10,"normal")
police1_15=("Cracked Code",15,"normal")
police1_20=("Cracked Code",20,"normal")
police1_50=("Cracked Code",50,"normal")

police2_10=("Times New Yorker",10,"normal")
police2_15=("Times New Yorker",15,"normal")
police2_20=("Times New Yorker",20,"normal")
police2_30=("Times New Yorker",30,"normal")
police2_50=("Times New Yorker",50,"normal")

localisation="menuPrincipal"
menu="menuPrincipal"
joueur=Joueur("Default","Default")
ennemi=Monstre()
listeBonus=["DPC","DPS","money","critique","esprit"]

fen=Fenetre(1400, 800)
fen.configFenetre("Infantry Squad Of Nerialvas 2", 1400, 800, 200, 5, False, False)

### IMAGES ###

fontMenuPrincipalI=PhotoImage(file="images/fonts/fontMenuPrincipal.png")
iconeMenuServantsI=PhotoImage(file="images/fenetre/iconeMenuServants.png")
iconeMenuEspritI=PhotoImage(file="images/fenetre/iconeMenuEsprit.png")
iconeMenuWarpI=PhotoImage(file="images/fenetre/iconeMenuWarp.png")


#temporaire
miseEnPlaceJeuI=PhotoImage(file="images/miseEnPlaceJeu.png")



#divers de la fenetre
fenetreDivers={"lvlUp":PhotoImage(file="images/fenetre/lvlup.png")}

fontsJeu=[]

for i in range(len(listdir("images/fonts/fontsJeu"))) :
    
    fontsJeu.append(PhotoImage(file="images/fonts/fontsJeu/font"+str(i)+".png"))
    
    
    
monstresI=[]

for i in range(len(listdir("images/monstres"))) :
    
    monstresI.append([])

    for j in range(len(listdir("images/monstres/stage"+str(i)))) :
        
        monstresI[i].append(PhotoImage(file="images/monstres/stage"+str(i)+"/"+str(j)+".png"))
        
        
        
servantsI={}

listeServantsINames=listdir("images/servants")

for i in range(len(listeServantsINames)) :
    
    servantsI[listeServantsINames[i]]=PhotoImage(file=("images/servants/"+listeServantsINames[i]))