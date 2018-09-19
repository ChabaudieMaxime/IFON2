############################ IMPORT ###########################################

from CHEST import Debug
from Classes import Joueur
from os import listdir
import pickle
import Const
import random

def verifierDisponibilitePseudo(pseudo):
    
    return Debug.existFic(pseudo, "comptes")


def enregistrerNouveauJoueur(pseudo,mdp):
    
    joueur=Joueur(pseudo, mdp)
    
    fichier=open('comptes/'+str(pseudo),'wb')
    
    pickle.dump(joueur, fichier)
    pickle.dump(Const.ennemi, fichier)
    
    
    fichier.close()
    
    Const.joueur=joueur
    
    
def chargerJoueur(nomFic):
    
    fichier=open('comptes/'+str(nomFic),"rb")
    
    Const.joueur=pickle.load(fichier)
    Const.ennemi=pickle.load(fichier)
    
    fichier.close()

def sauvegarderPartie():
    
    fichier=open("comptes/"+str(Const.joueur.nomJoueur),"wb")
    
    pickle.dump(Const.joueur, fichier)
    pickle.dump(Const.ennemi, fichier)
    
    fichier.close()

def getStageInGame():
    
    return int((Const.joueur.stage-1)%100/10)
        
def fontJeuIndex() :
    
    return int((Const.joueur.stage-1)%100/10)


def choisirIndexImageMonstre():
    
    return random.randint(0,len(listdir("images/monstres/stage"+str(getStageInGame())))-3)

def choisirImageMonstre():
    
    return Const.monstresI[getStageInGame()][choisirIndexImageMonstre()]
    

def definirStatusMonstre(etape,stage):
    
    if etape!=10 :
        
        return "basique"
        
    else :
        
        if stage%10==0 :
            
            return "superBoss"
        
        else : return "boss"


def definirPVMonstre(status,etape,stage):
    
    if status=="basique" :
        
        return (etape+stage*10+int((stage*stage)))
    
    elif status=="boss" :
        
        return (etape+stage*10+int((stage*stage)))*5
    
    elif status=="superBoss" :
        
        return (etape+stage*10+int((stage*stage)))*10
    
    
def definirGainMonstre(status,joueur,etape,stage):
    
    if status=="basique" :
        
        return int(((2*stage-verifEtapePourGain(etape))+10/100*stage)*(joueur.espritBonus["money"])/100)
    
    elif status=="boss" :

        return int(((2*stage-verifEtapePourGain(etape))+10/100*stage)*(joueur.espritBonus["money"])/100)*5
    
    elif status=="superBoss" :

        return int(((2*stage-verifEtapePourGain(etape))+10/100*stage)*(joueur.espritBonus["money"])/100)*10
    
    
def definirEspritMonstre(status,etape,stage,joueur):
    
    if status=="boss" :
        
        esprit=stage
        esprit+=int(stage*(joueur.espritBonus["esprit"]-100)/100)
        
        return esprit
    
    elif status=="superBoss" :
        
        esprit=stage
        esprit+=int(stage*(joueur.espritBonus["esprit"]-100)/100)
        return esprit*10
    
    else : return 0
    
    

def verifEtapePourGain(etape):
    
    if etape<5 :
        
        return 1
    
    else : return 0



def definirEtapeJoueur(etape):
    
    if etape==0 :
        
        return 1
    
    if etape < 10 :
        
        return etape+1
    
    else : return 1 
    
    

def definirStageJoueur(etape,stage):
    
    if stage==0 : 
        
        return 1
    
    if etape==1 :
        
        return stage+1
    
    else : return stage
    
    

def definirPrixEsprit(niveau):
    
    return niveau


def degatsAjoutesSiCoupCritique(degats):

    if (Const.joueur.espritBonus["critique"]-100)>random.randint(0,100) :
        
        return degats*10
    
    else : return 0



def formatEcritureNombre(nombre):
    
    unites=["","K","M","G"]
    
    compteurUnite=1000
    
    indiceFinal=0
    
    while nombre-compteurUnite>=0 :
        
        compteurUnite*=1000
        
        indiceFinal+=1
        
    if indiceFinal==0 :
    
        return "%d"%nombre+str(unites[indiceFinal])
    
    else :
        
        afficheur=str(nombre)
        
        if nombre-compteurUnite/10>=0 :
            
            return afficheur[0]+afficheur[1]+afficheur[2]+"."+afficheur[3]+unites[indiceFinal]
    
        elif nombre-compteurUnite/100>=0 :
            
            return afficheur[0]+afficheur[1]+"."+afficheur[2]+afficheur[3]+unites[indiceFinal]
        
        else : return afficheur[0]+"."+afficheur[1]+afficheur[2]+afficheur[3]+unites[indiceFinal]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        
        
    