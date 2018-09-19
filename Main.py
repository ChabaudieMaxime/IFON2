from CHEST import ZoneSaisie
import Const
import Proc
from Classes import Servant
from Const import fen
from threading import Thread
import time

############################# PROCEDURES ######################################

### PROCEDURE CHANGEMENT COULEUR TEXTES ###

def changerCouleurTexte(objet):

    couleur=fen.can.itemcget(objet, "fill")

    if couleur == "white" :

        fen.can.itemconfig(objet, fill="red")

    elif couleur == "red" :

        fen.can.itemconfig(objet, fill="white")



### PROCEDURE QUI GERE TOUTES LES INTERACTIONS AVEC LES MONSTRES ###

def attaquerMonstre(typeAttaque):

    if typeAttaque=="DPC" :

        degats=0

        servantsJoueur=Const.joueur.servants

        for i in range(len(servantsJoueur)):

            if servantsJoueur[i].status=="DPC" :

                degats+=servantsJoueur[i].degats

        degats+=Proc.degatsAjoutesSiCoupCritique(degats)

        Const.ennemi.PV-=degats

        miseAJourAffichagePVMonstre()

        if Const.ennemi.PV<=0 :

            gainDeMoneyEspritAuJoueur()

            changementEnnemi()



    elif typeAttaque=="DPS" :

        degats=0

        servantsJoueur=Const.joueur.servants

        for i in range(len(servantsJoueur)):

            if servantsJoueur[i].status=="DPS" :

                degats+=servantsJoueur[i].degats

        Const.ennemi.PV-=int(degats/10)

        miseAJourAffichagePVMonstre()

        if Const.ennemi.PV<=0 :

            gainDeMoneyEspritAuJoueur()

            changementEnnemi()



### PROCEDURE QUI GERE TOUS LES CALCULS ET LES CHANGEMENTS GRAPHIQUES LIES A LA MORT D'UN MONSTRE ET A L'APPARITION D'UN NOUVEAU ###

def changementEnnemi():

    joueur=Const.joueur

    joueur.etape=Proc.definirEtapeJoueur(joueur.etape)

    joueur.stage=Proc.definirStageJoueur(joueur.etape,joueur.stage)

    etape=joueur.etape

    stage=joueur.stage

    Const.ennemi.status=Proc.definirStatusMonstre(etape,stage)

    Const.ennemi.PV=Proc.definirPVMonstre(Const.ennemi.status,etape,stage)

    Const.ennemi.gain=Proc.definirGainMonstre(Const.ennemi.status,Const.joueur,etape,stage)

    Const.ennemi.gainEsprit=Proc.definirEspritMonstre(Const.ennemi.status, etape, stage, Const.joueur)

    miseAJourAffichageStageEtape()
    miseAJourAffichageMonnaie()
    changerImageMonstre()
    miseAJourAffichagePVMonstre()
    miseAJourAffichageFont()


### PROCEDURE QUI GERE TOUS LES CALCULS ET LES CHANGEMENTS GRAPHIQUES LIES AU GAIN DE MONEY A LA MORT D'UN MONSTRE ###

def gainDeMoneyEspritAuJoueur():

    Const.joueur.money+=Const.ennemi.gain

    Const.joueur.espritNonDisponible+=Const.ennemi.gainEsprit

### PROCEDURE QUI CHANGE L'IMAGE DU MONSTRE

def changerImageMonstre():

    if Const.ennemi.status=="basique" :

        fen.can.itemconfig("monstre", image=Const.monstresI[Proc.getStageInGame()][Proc.choisirIndexImageMonstre()])

    elif Const.ennemi.status=="boss" :

        fen.can.itemconfig("monstre", image=Const.monstresI[Proc.getStageInGame()][5])

    elif Const.ennemi.status=="superBoss" :

        fen.can.itemconfig("monstre", image=Const.monstresI[Proc.getStageInGame()][6])


### PRCODEDURE QUI GERE ENTIEREMENT LES ACTIONS D'UNE MONTEE DE NIVEAU D'UN ESPRIT ###

def monterNiveauEsprit(i,value):

    if value=="max" :

        while Const.joueur.esprit>=Const.joueur.espritPrix[i] :

            if i==Const.listeBonus[3] :

                Const.joueur.esprit-=Const.joueur.espritPrix[i]

                Const.joueur.espritNiveau[i]+=1

                Const.joueur.espritPrix[i]+=Proc.definirPrixEsprit(Const.joueur.espritNiveau[i])

                Const.joueur.espritBonus[i]=Const.joueur.espritBonus[i]+1

            else :
                Const.joueur.esprit-=Const.joueur.espritPrix[i]

                Const.joueur.espritNiveau[i]+=1

                Const.joueur.espritPrix[i]+=Proc.definirPrixEsprit(Const.joueur.espritNiveau[i])

                Const.joueur.espritBonus[i]=Const.joueur.espritBonus[i]+10
    else :
        
        compteur=0

        while compteur < value :

            if Const.joueur.esprit>=Const.joueur.espritPrix[i] :

                if i==Const.listeBonus[3] :

                    Const.joueur.esprit-=Const.joueur.espritPrix[i]

                    Const.joueur.espritNiveau[i]+=1

                    Const.joueur.espritPrix[i]+=Proc.definirPrixEsprit(Const.joueur.espritNiveau[i])

                    Const.joueur.espritBonus[i]=Const.joueur.espritBonus[i]+1

                else :
                    Const.joueur.esprit-=Const.joueur.espritPrix[i]

                    Const.joueur.espritNiveau[i]+=1

                    Const.joueur.espritPrix[i]+=Proc.definirPrixEsprit(Const.joueur.espritNiveau[i])

                    Const.joueur.espritBonus[i]=Const.joueur.espritBonus[i]+10
                    
            compteur+=1

    miseAJourAffichageEsprit()


### PROCEDURE QUI PREND EN COMPTE TOUS LES CALCULS ET LES CHANGEMENTS GRAPHIQUES LIES A LA MONTE DE NIVEAU D'UN SERVANT ###

def monterNiveauServant(i,value):

    servant= Const.joueur.servants[i]

    if value=="max" :

        while argentSuffisantPourLvlUp(servant) :

            payerPrixLvlUpServant(servant)

            servant.niveau+=1

            modifierMultiplicateurServant(servant)

            servant.degatsBase=servant.degatsBase+1+servant.degatsBase*servant.tauxUpDegats

            multiplicateur=int((servant.degatsBase*servant.multiplicateur)-servant.degatsBase)

            bonus=int((servant.degatsBase*(Const.joueur.espritBonus[servant.status]/100))-servant.degatsBase)

            servant.degats=int(servant.degatsBase)+multiplicateur+bonus

            modifierPrixServant(servant)

    else :
        
        compteur=0
        
        while compteur < value :

            if argentSuffisantPourLvlUp(servant) :

                payerPrixLvlUpServant(servant)

                servant.niveau+=1

                modifierMultiplicateurServant(servant)

                servant.degatsBase=servant.degatsBase+1+servant.degatsBase*servant.tauxUpDegats

                multiplicateur=int((servant.degatsBase*servant.multiplicateur)-servant.degatsBase)

                bonus=int((servant.degatsBase*(Const.joueur.espritBonus[servant.status]/100))-servant.degatsBase)

                servant.degats=int(servant.degatsBase)+multiplicateur+bonus

                modifierPrixServant(servant)
                
            compteur+=1

    miseAJOurAffichageNiveauDegatsPrixMultiplicateurServant(i)

    miseAJourAffichageMonnaie()


### PROCEDURE QUI GERE LA VERIFICATION DE L'ARGENT POUR QU'UN SERVANT PUISSE MONTER DE NIVEAU ###

def argentSuffisantPourLvlUp(servant):

    return Const.joueur.money>=servant.prix


### PROCEDURE QUI GERE LA MONTEE DE NIVEAU D'UN SERVANT AU NIVEAU DE LA MONNAIE ###

def payerPrixLvlUpServant(servant):

    Const.joueur.money-=servant.prix


### PROCEDURE QUI GERE LA MONTEE DU PRIX DU NIVEAU D'UN SERVANT ###

def modifierPrixServant(servant):

    servant.prixBase=servant.prixBase+2+servant.prixBase*servant.tauxUpPrix
    servant.prix=int(servant.prixBase)



### PROCEDURE QUI GERE LA MONTEE DU MULTIPLICATEUR D'UN SERVANT ###

def modifierMultiplicateurServant(servant):

    servant.multiplicateur+=0.001

    servant.multiplicateur=round(servant.multiplicateur,4)

### PROCEDURE QUI GERE LE WARP ###

def warp():

    servants=Const.joueur.servants

    multiplicateurs=[]

    Const.joueur.esprit+=Const.joueur.espritNonDisponible

    Const.joueur.espritNonDisponible=0

    Const.joueur.stage=0

    Const.joueur.etape=0

    Const.joueur.money=0

    changementEnnemi()

    for i in range(len(servants)):

        multiplicateurs.append(servants[i].multiplicateur)

    Const.joueur.servants=[Servant("player", "DPC", 0, 1, 10, 10, 0.05, 0.05),
                       Servant("morrant", "DPS", 0, 1, 10, 10, 0.05, 0.05)]

    for i in range(len(servants)):

        Const.joueur.servants[i].multiplicateur=multiplicateurs[i]
        miseAJOurAffichageNiveauDegatsPrixMultiplicateurServant(i)

    miseAJourAffichageEsprit()
    miseAJourAffichageFont()
    miseAJourAffichageMonnaie()
    miseAJourAffichagePVMonstre()
    miseAJourAffichageStageEtape()

### PROCEDURE QUI MET A JOUR L'FFICHAGE DU NIVEAU ET DES DEGATS D'UN SERVANT LORS DE LA MONTEE DE NIVEAU ###

def miseAJOurAffichageNiveauDegatsPrixMultiplicateurServant(i):

    nom=Const.joueur.servants[i].nom

    niveau=Const.joueur.servants[i].niveau

    degats=Const.joueur.servants[i].degats

    prix=Const.joueur.servants[i].prix

    multiplicateur=Const.joueur.servants[i].multiplicateur

    fen.can.itemconfig("servant_"+str(nom)+"nom",  text=nom.upper()+"  LVL : "+str(niveau))

    fen.can.itemconfig("servant_"+str(nom)+"degats",  text=str(Const.joueur.servants[i].status)+" : "+Proc.formatEcritureNombre(degats))

    fen.can.itemconfig("servant_"+str(nom)+"prix",  text="Prix : "+Proc.formatEcritureNombre(prix))

    fen.can.itemconfig("servant_"+str(nom)+"multiplicateur",  text="PowUp : x"+str(multiplicateur))

def miseAJourAffichageStageEtape():

    fen.can.itemconfig("stageTexte", text="STAGE  :  "+str(Const.joueur.stage)+"."+str(Const.joueur.etape))


### PROCEDURE QUI MET A JOUR L'AFFICHAGE DES MONNAIES DISPONIBLES ###

def miseAJourAffichageMonnaie():

    fen.can.itemconfig("moneyTexte", text="money :  "+Proc.formatEcritureNombre(Const.joueur.money))

### PROCEDURE QUI MET A JOUR L'AFFICHAGE DES ESPRITS ###

def miseAJourAffichageEsprit():

    fen.can.itemconfig("espritTexte", text="Esprits : "+Proc.formatEcritureNombre(Const.joueur.esprit))

    texte=["DPC actuel : +","DPS atcuel : +","Monnaie actuelle : +","Taux critique actuel : ","Esprits actuels : +"]

    for i in range (len(Const.joueur.espritBonus)) :

        tagNomValue=Const.listeBonus[i]+"_nomValue"

        tagPrix=Const.listeBonus[i]+"_prix"

        fen.can.itemconfig(tagNomValue, text=texte[i]+Proc.formatEcritureNombre(Const.joueur.espritBonus[Const.listeBonus[i]]-100)+"%")

        niveauActuelEsprit=Const.joueur.espritNiveau[Const.listeBonus[i]]

        niveauLimiteEsprit=Const.joueur.espritLimiteNiveau[Const.listeBonus[i]]

        if niveauActuelEsprit<niveauLimiteEsprit or niveauLimiteEsprit==0:

            fen.can.itemconfig(tagPrix, text="Prix : "+Proc.formatEcritureNombre(Const.joueur.espritPrix[Const.listeBonus[i]]))

        if niveauActuelEsprit>=niveauLimiteEsprit and niveauLimiteEsprit!=0:

            try :

                tagPrix=Const.listeBonus[i]+"_prix"

                tagLvlUp=Const.listeBonus[i]+"_lvlUp"

                fen.detruire(tagPrix)
                fen.detruire(tagLvlUp)

            except KeyError : pass

###PROCEDURE QUI MET A JOUR L'AFFICHAGE DES PV DU MONSTRE ###

def miseAJourAffichagePVMonstre():

    fen.can.itemconfig("textePVMonstre", text="PV : "+Proc.formatEcritureNombre(Const.ennemi.PV))

###PROCEDURE QUI MET A JOUR L'AFFICHAGE DU FONT DE JEU ###

def miseAJourAffichageFont():

    fen.can.itemconfig("fontJeu", image=Const.fontsJeu[Proc.fontJeuIndex()])

###PROCEDURE QUI EFFACE ENTIEREMENT L'AFFICHAGE DES SERVANTD ###

def effacerMenuServants():

    for i in range(len(Const.joueur.servants)):

        nom=Const.joueur.servants[i].nom

        tagImg="servant_"+str(nom)+"I"

        tagNom="servant_"+str(nom)+"nom"

        tagLvlUp="servant_"+str(nom)+"lvlUp"

        tagDegats="servant_"+str(nom)+"degats"

        tagPrix="servant_"+str(nom)+"prix"

        tagMultiplicateur="servant_"+str(nom)+"multiplicateur"

        fen.detruire(tagImg)
        fen.detruire(tagNom)
        fen.detruire(tagLvlUp)
        fen.detruire(tagDegats)
        fen.detruire(tagPrix)
        fen.detruire(tagMultiplicateur)


def effacerMenuEsprit():

    for i in range (len(Const.joueur.espritBonus)) :

        tagNomValue=Const.listeBonus[i]+"_nomValue"

        tagPrix=Const.listeBonus[i]+"_prix"

        tagLvlUp=Const.listeBonus[i]+"_lvlUp"

        fen.detruire(tagNomValue)

        try :
            fen.detruire(tagPrix)
            fen.detruire(tagLvlUp)
        except KeyError : pass

### CHANGER LA LOCALISATION DE LA FENETRE ( UPDATE DE L'AFFICHAGE ) ###

def changerLocalisationFenetre(nouvelleLocalisation):

    ## menu principal ##

    if Const.localisation == "menuPrincipal" :

        # Retour #

        if nouvelleLocalisation== "menuPrincipal" :

            fen.reinitialiserObjet()

            fen.ajouter("fontMenuPrincipal",fen.can.create_image(702,402,image=Const.fontMenuPrincipalI,tag="fontMenuPrincipal"))

            fen.ajouter("texteCommencer", fen.can.create_text(700,300,text="COMMENCER",font=Const.police1_20,fill="white",tag="texteCommencer"))
            fen.ajouter("texteCharger", fen.can.create_text(700,400,text="CHARGER",font=Const.police1_20,fill="white",tag="texteCharger"))
            fen.ajouter("texteQuitter", fen.can.create_text(700,500,text="QUITTER",font=Const.police1_20,fill="white",tag="texteQuitter"))

        else :

            if nouvelleLocalisation == "joueurCharge" :

                fen.detruire("retourMenuPrincipal")

            else :

                if "retourMenuPrincipal" not in fen.object.keys() :

                    fen.ajouter("retourMenuPrincipal", fen.can.create_text(700,400,text="RETOUR",font=Const.police1_20,fill="white",tag="retourMenuPrincipal"))

                    fen.can.tag_bind("retourMenuPrincipal", "<Button-1>", lambda use : changerLocalisationFenetre("menuPrincipal"))
                    fen.can.tag_bind("retourMenuPrincipal","<Enter>", lambda use : changerCouleurTexte("retourMenuPrincipal"))
                    fen.can.tag_bind("retourMenuPrincipal","<Leave>", lambda use : changerCouleurTexte("retourMenuPrincipal"))


        # commencer #

        if Const.menu == "menuPrincipal" and nouvelleLocalisation== "creerNouveauJoueurNom" :

            fen.detruire("texteCommencer")
            fen.detruire("texteCharger")

            fen.ajouter("zoneSaisieCompteNom", ZoneSaisie(fen, 400, 300, 1000, "NOM DU JOUEUR", 15))
            fen.fenetre.bind("<Return>", lambda use : creerNouveauJoueur())


        elif Const.menu == "creerNouveauJoueurNom" and nouvelleLocalisation== "creerNouveauJoueurMDP" :

            fen.object["zoneSaisieCompteNom"].destructionZoneSaisie()
            fen.fenetre.unbind_all("<Key>")
            fen.ajouter("zoneSaisieCompteMDP", ZoneSaisie(fen, 400, 300, 1000, "MDP DU JOUEUR", 15))
            fen.fenetre.bind("<Return>", lambda use : creerNouveauJoueur())


        elif Const.menu == "creerNouveauJoueurNom" and nouvelleLocalisation== "creerNouveauJoueurNom" :

            fen.object["zoneSaisieCompteNom"].destructionZoneSaisie()
            fen.fenetre.unbind_all("<Key>")
            fen.ajouter("zoneSaisieCompteNom", ZoneSaisie(fen, 400, 300, 1000, "NOM DEJA PRIS", 15))
            fen.fenetre.bind("<Return>", lambda use : creerNouveauJoueur())


        # joueur chargé #


        elif  nouvelleLocalisation== "joueurCharge" :

            if Const.menu == "creerNouveauJoueurMDP" :

                fen.object["zoneSaisieCompteMDP"].destructionZoneSaisie()
                fen.fenetre.unbind_all("<Key>")

            elif Const.menu == "chargerJoueurMDP" :

                fen.object["zoneSaisieChargerMDP"].destructionZoneSaisie()
                fen.fenetre.unbind_all("<Key>")

            nomJoueur=Const.joueur.nomJoueur

            fen.fenetre.unbind("<Return>")

            fen.ajouter("nomJoueurMenuPrincipal", fen.can.create_text(700,200,text="BIENVENUE "+nomJoueur.upper(),font=Const.police1_20,fill="white",tag="nomJoueurMenuPrincipal"))
            fen.ajouter("jouerMenuPrincipal", fen.can.create_text(700,400,text="JOUER",font=Const.police1_20,fill="white",tag="jouerMenuPrincipal"))

            fen.can.tag_bind("nomJoueurMenuPrincipal","<Enter>", lambda use : changerCouleurTexte("nomJoueurMenuPrincipal"))
            fen.can.tag_bind("nomJoueurMenuPrincipal","<Leave>", lambda use : changerCouleurTexte("nomJoueurMenuPrincipal"))

            fen.can.tag_bind("jouerMenuPrincipal", "<Button-1>", lambda use : lancementJeu())
            fen.can.tag_bind("jouerMenuPrincipal","<Enter>", lambda use : changerCouleurTexte("jouerMenuPrincipal"))
            fen.can.tag_bind("jouerMenuPrincipal","<Leave>", lambda use : changerCouleurTexte("jouerMenuPrincipal"))


        # charger joueur #

        elif Const.menu == "menuPrincipal" and nouvelleLocalisation== "chargerJoueurNom" :
            fen.detruire("texteCommencer")
            fen.detruire("texteCharger")

            fen.ajouter("zoneSaisieChargerNom", ZoneSaisie(fen, 400, 300, 1000, "NOM DU JOUEUR", 15))
            fen.fenetre.bind("<Return>", lambda use : chargerJoueur())


        elif Const.menu == "chargerJoueurNom" and nouvelleLocalisation== "chargerJoueurNom" :

            fen.object["zoneSaisieChargerNom"].destructionZoneSaisie()
            fen.fenetre.unbind_all("<Key>")
            fen.ajouter("zoneSaisieChargerNom", ZoneSaisie(fen, 400, 300, 1000, "NOM INVALIDE", 15))
            fen.fenetre.bind("<Return>", lambda use : chargerJoueur())


        elif Const.menu == "chargerJoueurNom" and nouvelleLocalisation== "chargerJoueurMDP" :

            fen.object["zoneSaisieChargerNom"].destructionZoneSaisie()
            fen.fenetre.unbind_all("<Key>")
            fen.ajouter("zoneSaisieChargerMDP", ZoneSaisie(fen, 400, 300, 1000, "MDP DU JOUEUR", 15))
            fen.fenetre.bind("<Return>", lambda use : chargerJoueur())


        elif Const.menu == "chargerJoueurMDP" and nouvelleLocalisation== "chargerJoueurMDP" :

            fen.object["zoneSaisieChargerMDP"].destructionZoneSaisie()
            fen.fenetre.unbind_all("<Key>")
            fen.ajouter("zoneSaisieChargerMDP", ZoneSaisie(fen, 400, 300, 1000, "MOT DE PASSE FAUX", 15))
            fen.fenetre.bind("<Return>", lambda use : chargerJoueur())


    elif Const.localisation=="jeu" :

        if Const.menu=="joueurCharge" :

            fen.reinitialiserObjet()

            fen.ajouter("fontJeu", fen.can.create_image(702,402,image=Const.fontsJeu[Proc.fontJeuIndex()], tag="fontJeu"))
            fen.ajouter("miseEnPlaceJeu", fen.can.create_image(702,402,image=Const.miseEnPlaceJeuI))

            miseEnPlaceMenu()
            miseEnPlaceMonstre()
            miseEnPlaceServants()
            miseEnPlaceAffichageInfos()
            process["DPS"].start()

        # changements graphiques des menus en jeu

        elif Const.menu== "jeuServants" and nouvelleLocalisation== "jeuEsprit" :

            effacerMenuServants()
            miseEnPlaceEsprit()

        elif Const.menu== "jeuEsprit" and nouvelleLocalisation== "jeuServants" :

            effacerMenuEsprit()
            miseEnPlaceServants()
            for i in range(len(Const.joueur.servants)):
                miseAJOurAffichageNiveauDegatsPrixMultiplicateurServant(i)

    Const.menu=nouvelleLocalisation

### MISE EN PLACE DU MENU DANS LA FENETRE DE JEU ###

def miseEnPlaceMenu():

    x,y=1250,770

    fen.ajouter("quitterJeu", fen.can.create_text(x,y,text="QUITTER", font=Const.police2_30, fill="white", tag="quitterJeu"))

    fen.can.tag_bind("quitterJeu", "<Button-1>", lambda use : quitterJeu())
    fen.can.tag_bind("quitterJeu", "<Enter>", lambda use : changerCouleurTexte("quitterJeu"))
    fen.can.tag_bind("quitterJeu", "<Leave>", lambda use : changerCouleurTexte("quitterJeu"))

    y-=70
    fen.ajouter("sauvegarderJeu", fen.can.create_text(x,y,text="SAUVEGARDER", font=Const.police2_30, fill="white", tag="sauvegarderJeu"))

    fen.can.tag_bind("sauvegarderJeu", "<Button-1>", lambda use : Proc.sauvegarderPartie())
    fen.can.tag_bind("sauvegarderJeu", "<Enter>", lambda use : changerCouleurTexte("sauvegarderJeu"))
    fen.can.tag_bind("sauvegarderJeu", "<Leave>", lambda use : changerCouleurTexte("sauvegarderJeu"))

    x,y=527,152

    fen.ajouter("menuServants", fen.can.create_image(x,y,image=Const.iconeMenuServantsI, tag="menuServants"))
    fen.can.tag_bind("menuServants", "<Button-1>", lambda use : changerLocalisationFenetre("jeuServants"))

    y+=100

    fen.ajouter("menuEsprit", fen.can.create_image(x,y,image=Const.iconeMenuEspritI, tag="menuEsprit"))
    fen.can.tag_bind("menuEsprit", "<Button-1>", lambda use : changerLocalisationFenetre("jeuEsprit"))

    y+=100

    fen.ajouter("menuWarp", fen.can.create_image(x,y,image=Const.iconeMenuWarpI, tag="menuWarp"))
    fen.can.tag_bind("menuWarp", "<Button-1>", lambda use : warp())

    x,y=120,690

    fen.ajouter("modeLevelUpTexte", fen.can.create_text(x,y,text="Mode de LvlUp : ",font=Const.police2_20,tag="modeLevelUpTexte"))

    x+=150

    fen.ajouter("modeLevelUpx1", fen.can.create_text(x,y,text="X1",font=Const.police2_20,tag="modeLevelUpx1"))
    fen.can.tag_bind("modeLevelUpx1", "<Button-1>", lambda use : changerModeLevelUp(1))

    x+=100

    fen.ajouter("modeLevelUpx10", fen.can.create_text(x,y,text="X10",font=Const.police2_20,tag="modeLevelUpx10"))
    fen.can.tag_bind("modeLevelUpx10", "<Button-1>", lambda use : changerModeLevelUp(10))

    x+=100

    fen.ajouter("modeLevelUpxmax", fen.can.create_text(x,y,text="Max",font=Const.police2_20,tag="modeLevelUpxmax"))
    fen.can.tag_bind("modeLevelUpxmax", "<Button-1>", lambda use : changerModeLevelUp("max"))
    
    changerCouleurTexteLevelUp(Const.joueur.modeLvlUp)

### MISE EN PLACE DU MONSTRE DANS LA FENETRE PRINCIPALE DU JEU ###

def miseEnPlaceMonstre():

    fen.ajouter("monstre", fen.can.create_image(750,650,image=Proc.choisirImageMonstre(), tag="monstre"))
    fen.can.tag_bind("monstre", "<Button-1>", lambda use : attaquerMonstre("DPC"))

    x=700
    y=450

    fen.ajouter("textePVMonstre", fen.can.create_text(x,y,text="PV : "+Proc.formatEcritureNombre(Const.ennemi.PV), font=Const.police2_30, fill="white", anchor="w", tag="textePVMonstre"))


### MISE EN PLACE DES SERVANTS DANS LA FENETRE PRINCIPALE DU JEU ###

def miseEnPlaceServants():

    xImage,yImage=55,150

    xNomLvl,yNomLvl=255,130

    xLvlUp,yLvlUp=470,150

    xDegats,yDegats=230,160

    xPrix,yPrix=190,190

    xMultiplicateur,yMultiplicateur=360,190

    for i in range(len(Const.joueur.servants)) :

        nom=Const.joueur.servants[i].nom

        niveau=Const.joueur.servants[i].niveau

        status=Const.joueur.servants[i].status

        degats=Const.joueur.servants[i].degats

        prix=Const.joueur.servants[i].prix

        multiplicateur=Const.joueur.servants[i].multiplicateur

        imgServant=Const.servantsI[nom+".png"]

        tagImg="servant_"+str(nom)+"I"

        tagNom="servant_"+str(nom)+"nom"

        tagLvlUp="servant_"+str(nom)+"lvlUp"

        tagDegats="servant_"+str(nom)+"degats"

        tagPrix="servant_"+str(nom)+"prix"

        tagMultiplicateur="servant_"+str(nom)+"multiplicateur"

        fen.ajouter(tagImg, fen.can.create_image( xImage, yImage, image=imgServant, tag=tagImg))

        fen.ajouter(tagNom, fen.can.create_text( xNomLvl, yNomLvl, text=nom.upper()+"  LVL : "+str(niveau),  font=Const.police2_20, fill="black", tag=tagNom))

        fen.ajouter(tagLvlUp, fen.can.create_image( xLvlUp, yLvlUp, image=Const.fenetreDivers["lvlUp"], tag=tagLvlUp))

        fen.ajouter(tagDegats, fen.can.create_text( xDegats, yDegats, text=str(status)+" : "+Proc.formatEcritureNombre(degats),  font=Const.police2_20, fill="black", tag=tagDegats))

        fen.ajouter(tagPrix, fen.can.create_text( xPrix, yPrix, text="Prix : "+Proc.formatEcritureNombre(prix), font=Const.police2_20, fill="black", tag=tagPrix))

        fen.ajouter(tagMultiplicateur, fen.can.create_text(xMultiplicateur, yMultiplicateur, text="PowUp : x"+str(multiplicateur),  font=Const.police2_20, fill="black", tag=tagMultiplicateur))


        binderBouttonLevelUpServant(tagLvlUp,i,Const.joueur.modeLvlUp)

        yImage+=120

        yNomLvl+=120

        yLvlUp+=120

        yDegats+=120

        yPrix+=120

        yMultiplicateur+=120


### PROCEDURE QUI MET EN PLACE LES AFFICHAGES D'INFOS COMME LE STAGE OU AUTRES ###

def miseEnPlaceAffichageInfos():

    x,y=250,780

    fen.ajouter("stageTexte", fen.can.create_text(x,y,text="STAGE  :  "+str(Const.joueur.stage)+"."+str(Const.joueur.etape), font=Const.police2_30, fill="black", tag="stageTexte"))

    y-=50

    fen.ajouter("espritTexte", fen.can.create_text(x,y,text="Esprits : "+Proc.formatEcritureNombre(Const.joueur.esprit), font=Const.police2_30, fill="black", tag="espritTexte"))

    x=250
    y=50

    fen.ajouter("moneyTexte", fen.can.create_text(x,y,text="money :    "+Proc.formatEcritureNombre(Const.joueur.money), font=Const.police2_30, fill="black", tag="moneyTexte"))



### PROCEDURE QUI MET EN PLACE L'AFFICHAGE DES BONUS ESPRITS ET LEUR LEVEL UP ###

def miseEnPlaceEsprit():

    xNomValue,yNomValue=250,130

    xPrix,yPrix=200,160

    xLvlUp,yLvlUp=470,150

    texte=["DPC actuel : +","DPS atcuel : +","Monnaie actuelle : +","Taux critique actuel : ","Esprits actuels : +"]

    for i in range (len(Const.joueur.espritBonus)) :

        tagNomValue=Const.listeBonus[i]+"_nomValue"

        tagPrix=Const.listeBonus[i]+"_prix"

        tagLvlUp=Const.listeBonus[i]+"_lvlUp"

        fen.ajouter(tagNomValue, fen.can.create_text(xNomValue,yNomValue, text=texte[i]+Proc.formatEcritureNombre(Const.joueur.espritBonus[Const.listeBonus[i]]-100)+"%", font=Const.police2_20, fill="black",tag=tagNomValue))

        niveauActuelEsprit=Const.joueur.espritNiveau[Const.listeBonus[i]]

        niveauLimiteEsprit=Const.joueur.espritLimiteNiveau[Const.listeBonus[i]]

        if niveauActuelEsprit<niveauLimiteEsprit or niveauLimiteEsprit==0:

            fen.ajouter(tagPrix, fen.can.create_text(xPrix,yPrix, text="Prix : "+Proc.formatEcritureNombre(Const.joueur.espritPrix[Const.listeBonus[i]]), font=Const.police2_20, fill="black", tag=tagPrix))

            fen.ajouter(tagLvlUp, fen.can.create_image(xLvlUp,yLvlUp, image=Const.fenetreDivers["lvlUp"], tag=tagLvlUp))

        yNomValue+=80

        yPrix+=80

        yLvlUp+=80

        binderBoutonLevelUpEsprit(tagLvlUp,Const.listeBonus[i],Const.joueur.modeLvlUp)

### PROCEDURE POUR QUITTER LE JEU ###

def quitterJeu():

    Proc.sauvegarderPartie()

    fen.destruction()

### PROCEDURE QUI MET EN PLACE LA FENETRE DE JEU ###

def lancementJeu():

    Const.localisation="jeu"

    changerLocalisationFenetre("jeuServants")

### PROCEDURE CREATION D'UN NOUVEAU JOUEUR ###

def creerNouveauJoueur():

    if Const.menu != "creerNouveauJoueurNom" and Const.menu != "creerNouveauJoueurMDP" :
        changerLocalisationFenetre("creerNouveauJoueurNom")

    elif Const.menu == "creerNouveauJoueurNom" :

        pseudoAVerifier=fen.object["zoneSaisieCompteNom"].getZoneSaisie()

        pseudoPrit=Proc.verifierDisponibilitePseudo(pseudoAVerifier)

        if pseudoPrit is False :
            Const.joueur=pseudoAVerifier
            changerLocalisationFenetre("creerNouveauJoueurMDP")

        else : changerLocalisationFenetre("creerNouveauJoueurNom")

    elif Const.menu == "creerNouveauJoueurMDP" :

        nomJoueur=Const.joueur
        mdpJoueur=fen.object["zoneSaisieCompteMDP"].getZoneSaisie()
        Proc.enregistrerNouveauJoueur(nomJoueur,mdpJoueur)
        changerLocalisationFenetre("joueurCharge")

### PROCEDURE DE CHARGEMENT D'UN JOUEUR

def chargerJoueur():

    if Const.menu != "chargerJoueurNom" and Const.menu!= "chargerJoueurMDP" :
        changerLocalisationFenetre("chargerJoueurNom")

    elif Const.menu=="chargerJoueurNom" :

        pseudoAVerifier=fen.object["zoneSaisieChargerNom"].getZoneSaisie()

        pseudoUtilise=Proc.verifierDisponibilitePseudo(pseudoAVerifier)

        if pseudoUtilise :

            Const.joueur=pseudoAVerifier
            changerLocalisationFenetre("chargerJoueurMDP")

        else : changerLocalisationFenetre("chargerJoueurNom")

    elif Const.menu=="chargerJoueurMDP" :

        mdp=fen.object["zoneSaisieChargerMDP"].getZoneSaisie()

        Proc.chargerJoueur(Const.joueur)

        if Const.joueur.motDePasse==mdp :
            changerLocalisationFenetre("joueurCharge")

        else :
            Const.joueur=Const.joueur.nomJoueur
            changerLocalisationFenetre("chargerJoueurMDP")


### PROCEDURE QUI PERMET DE CHANGER LE MODE DE LEVEL UP ###

def changerModeLevelUp(mode):

    Const.joueur.modeLvlUp=mode
    
    if Const.menu=="jeuServants" :

        effacerMenuServants()
        miseEnPlaceServants()
        changerCouleurTexteLevelUp(mode)
        
    elif Const.menu=="jeuEsprit" :
        
        effacerMenuEsprit()
        miseEnPlaceEsprit()
        changerCouleurTexteLevelUp(mode)


### PROCEDURE QUI CHANGE LA COULEUR DU TEXTE DE MODE DE LEVEL UP ###

def changerCouleurTexteLevelUp(tag):

    listeTags=[1,10,"max"]
    
    for i in listeTags :
        
        if tag==i :
            
            fen.can.itemconfig("modeLevelUpx"+str(i), fill="red")
        
        else :
            
            fen.can.itemconfig("modeLevelUpx"+str(i), fill="black")
### ZONE DES BINDS ###

def binderBouttonLevelUpServant(tagLvlUp,i,value):

    fen.can.tag_bind(tagLvlUp, "<Button-1>", lambda use : monterNiveauServant(i,value))

def binderBoutonLevelUpEsprit(tagLvlUp,i,value):

    fen.can.tag_bind(tagLvlUp,"<Button-1>", lambda use : monterNiveauEsprit(i,value))

### ZONE DU THREAD DPS ###

class DPS (Thread):

    def __init__(self):

        Thread.__init__(self)
        self.valueStop=0

    def run(self):

        while self.valueStop==0 :
            try :
                time.sleep(0.1)
                attaquerMonstre("DPS")
            except RuntimeError : self.valueStop=1



### ZONE DE DECLARATION DES DIFFERENTS PROCESS ###

process={"DPS":DPS()}

### MENU PRINCIPAL ###

fen.ajouter("fontMenuPrincipal",fen.can.create_image(702,402,image=Const.fontMenuPrincipalI,tag="fontMenuPrincipal"))

fen.ajouter("texteCommencer", fen.can.create_text(700,300,text="COMMENCER",font=Const.police1_20,fill="white",tag="texteCommencer"))
fen.ajouter("texteCharger", fen.can.create_text(700,400,text="CHARGER",font=Const.police1_20,fill="white",tag="texteCharger"))
fen.ajouter("texteQuitter", fen.can.create_text(700,500,text="QUITTER",font=Const.police1_20,fill="white",tag="texteQuitter"))
fen.ajouter("version", fen.can.create_text(700,780,text="VERSION : "+Const.version,font=Const.police1_10,fill="white"))

fen.can.tag_bind("texteCommencer","<Button-1>", lambda use : creerNouveauJoueur())
fen.can.tag_bind("texteCommencer","<Enter>", lambda use : changerCouleurTexte("texteCommencer"))
fen.can.tag_bind("texteCommencer","<Leave>", lambda use : changerCouleurTexte("texteCommencer"))

fen.can.tag_bind("texteCharger","<Button-1>", lambda use : chargerJoueur())
fen.can.tag_bind("texteCharger","<Enter>", lambda use : changerCouleurTexte("texteCharger"))
fen.can.tag_bind("texteCharger","<Leave>", lambda use : changerCouleurTexte("texteCharger"))

fen.can.tag_bind("texteQuitter","<Button-1>", lambda use :fen.destruction())
fen.can.tag_bind("texteQuitter","<Enter>", lambda use : changerCouleurTexte("texteQuitter"))
fen.can.tag_bind("texteQuitter","<Leave>", lambda use : changerCouleurTexte("texteQuitter"))

fen.lancement()
