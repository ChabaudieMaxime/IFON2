from threading import Thread
class Fenetre :

    def __init__(self,canvasX=500,canvasY=500,couleurFont="default"):
        
        """ 
        INFORMATIONS : 
        - Initialisation de la fenetre, du canvas. modification de la couleur du font du canvas seulement
        - Initialisation de la liste d'objets et des objetInterne ( non modifiable hors classe )
        - Initialisation du placement du canvas avec coordonnées -2,-2 pour centrer le canvas sur la fenetre
        """

        from tkinter import Tk,Canvas

        self.fenetre=Tk()
        if couleurFont=="default" : self.can=Canvas(self.fenetre,width=canvasX,height=canvasY)
        else : self.can=Canvas(self.fenetre,width=canvasX,height=canvasY,background=couleurFont)
        self.can.place(x=-2,y=-2)
        self.object={}
        self.objectInterne={}

    def lancement(self):

        self.fenetre.mainloop()


    def cacher(self):

        self.fenetre.state('withdrawn')


    def montrer(self):

        self.fenetre.state('normal')


    def destruction(self):

        self.fenetre.quit()


    def configFenetre(self,titreFenetre="Default",longueurFenetre=500,largeurFenetre=500,distanceXFenetre=0,distanceYFenetre=0,redimension=False,typeEcran=False):
        
        """ 
        
        INFORMATIONS : 
        
        - argument redimension par défaut à false bloque le redimensionnement de la fenetre
        - argument typeEcran par défaut à false règle la fenêtre ( à false, la fenetre est une fenetre window basique, à true c'est une fenetre pleine )
        
        """
        self.fenetre.title(titreFenetre)
        self.fenetre.geometry(str(longueurFenetre)+"x"+str(largeurFenetre)+"+"+str(distanceXFenetre)+"+"+str(distanceYFenetre))
        self.fenetre.wm_resizable(redimension, redimension)
        self.fenetre.overrideredirect(typeEcran)


    def replacement(self,newX=-2,newY=-2):

        self.can.place(x=newX,y=newY)
        

    def redimensionneCanvas(self,newX,newY):

        self.can.config(width=newX,height=newY)
        
    def ajouter(self,name,objetCree):
        
        if type(name)!=str : raise AttributeError("Le nom doit obligatoirement être une string")
        
        self.object[name]=objetCree
    
    
    def ajouterTexte(self,identifiant,posX,posY,texte,police=("Arial",12),couleur="black"):
        
        self.ajouter(identifiant, self.can.create_text( posX, posY, text=texte, font=police, fill=couleur, tag=identifiant))
    
    def ajouterImage(self,identifiant,posX,posY,image):
        
        self.ajouter(identifiant, self.can.create_image( posX, posY, image=image, tag=identifiant ))
        
    def detruire(self,ID):
        
        if type(ID)==str : 
            
            if ID not in self.object :
                
                raise RuntimeError("L'identifiant n'existe pas")
            
            else :
                
                if type(self.object[ID])==list :
                    
                    for i in range(len(self.object[ID])) :
                        
                        self.can.delete(self.object[ID][i])
                        
                else :
                
                    self.can.delete(self.object[ID])
                
                del self.object[ID]
            
        else : raise AttributeError("L'identifiant doit obligatoirement être une string")
        
    def reinitialiserObjet(self):
        
        from tkinter import ALL
        
        self.can.delete(ALL)
            
        self.objectIndex={}
        
        
class ZoneSaisie :
    
    """
    COMPATIBLE SEULEMENT AVEC L'OBJET FENETRE
    """
    
    def __init__(self,fenetre,departX,departY,finX,text="Entrez du texte",longueurMaxMot=15,policeText=("Arial",20,"normal"),couleurFont="#4c4c4c",couleurText="#ededed",epaisseur=50):
        
        """ 
        INFORMATIONS :
        - Si la longueurMaxMot est laissée par défaut, elle est adaptée automatiquement au nombre de lettres que peut contenir la zone de saisie
        - Format policeText UNIQUEMENT en tuple ou STRING
        - Taille de police OBLIGATOIREMENT inférieure à 25 pour éviter tout problème graphique
        """
        
        longueur=finX-departX
        
        longueurText=int(longueur/30)
        
        if longueurMaxMot==15 :
            
            longueurMaxMot=longueurText
            
            
        #Gestion des exceptions
        if len(text)>longueurText : raise ValueError ("Problème avec le texte à afficher avant la saisie, taille maximale du texte : "+str(longueurText))
        if longueurMaxMot > longueurText : raise ValueError ("Longueur max du mot dépasse la taille graphique de la fenetre. Longueur max possible pour vos paramètres : "+str(longueurText))
        if type(policeText)!=tuple and type(policeText)!=str : raise AttributeError("Mauvais format, doit être de type Tuple ou String")
        if type(policeText)==tuple : 
            if len(policeText)>3: raise AttributeError("Trop d'attributs dans le Tuple")
            if len(policeText)<2 : raise AttributeError("Pas assez d'attributs dans le tuple")
            if type(policeText[0])!=str : raise AttributeError("Le premier attribut du tuple doit être de type String")
            if type(policeText[1])!=int : raise AttributeError("Le deuxième attribut du tuple doit être de type Int")
            
        
        #Creation de la zone de saisie
        self.zoneGraph=fenetre.can.create_line(departX,departY,finX,departY,width=epaisseur,fill=couleurFont)
        self.zoneText=fenetre.can.create_text(departX+longueur/2,departY,text=text,font=policeText,fill=couleurText)
        self.text=""
        self.longueurMot=longueurMaxMot
        self.fenetre=fenetre
        
        fenetre.fenetre.bind_all("<Key>", self.gestionSaisie)
        
    
    def gestionSaisie(self,event):
        
        #Liste des caractères autorisés
        #Exceptions gérées plus bas
        charAutorise=["a","z","e","r","t","y","u","i","o","p","q","s","d","f","g","h","j","k","l","m","w","x","c","v","b","n",
                      "0","1","2","3","4","5","6","7","8","9",
                      "A","Z","E","R","T","Y","U","I","O","P","Q","S","D","F","G","H","J","K","L","M","W","X","C","V","B","N"]
        
        
        i=0
        
        lettre=""
        
        #Effacement d'une lettre
        #IndexError d'une liste vide géré
        
        if event.keysym=="BackSpace" and len(self.text)>0 :
                
            self.text=self.text[:-1]
                
        
        #Verification de la longueur de la saisie
        #Pour éviter un dépassement graphique
        elif len(self.text)<self.longueurMot and event.keysym!="BackSpace":
            
            #Parcourt de la liste des charAutorisés si l'event est présent.
            while i<len(charAutorise) and lettre=="":
                
                if event.keysym==charAutorise[i] :
                    
                    lettre=event.keysym
                i+=1
                
                
            #Bloc pour espace, é, -, virgule. 
            if event.keysym=="space" :
                
                lettre=" "
                
            elif event.keysym=="ecaute" :
                
                lettre="é"
                
            elif event.keysym=="minus" :
                
                lettre="-"
                
            elif event.keysym=="comma" :
                
                lettre=","
                
                
            #Si l'event a été trouvé avant
            #Rajout de la lettre dans la saisie + mise à jour graphique
            if lettre!="" :
                
                self.text+=lettre
                
        self.fenetre.can.itemconfig(self.zoneText, text=self.text)
             
    
    def unbind(self):
        
        self.fenetre.unbind_all("<Key>")
        
    def getZoneSaisie(self):
        
        return self.text
    
    def destructionZoneSaisie(self):
        
        self.fenetre.can.delete(self.zoneGraph,self.zoneText)
        del self
        
        
class Animation(Thread):
    
    """
    COMPATIBLE SEULEMENT AVEC L'OBJET FENETRE
    """
    
    def __init__(self,fenetre,objet,images,intervalle=1):
        
        """
        INITIALISE L'ANIMATION. NECESSITE POUR FONCTIONNER :
        -une Fenetre
        -une référence à la variable de l'animation ( pas forcément contenue dans l'object de la Fenetre )
        -une liste d'images ( au moins 2 )
        -un intervalle entre chaque changement d'image ( au moins 0.0001 )
        """
        
        Thread.__init__(self)
        if intervalle<=0 : raise AttributeError("Le temps d'intervalle entre 2 images doit être supérieur à 0")
        if len(images)<=1 : raise AttributeError("Le nombre d'images de la liste doit être d'au moins 2")
        
        self.images=images
        self.intervalle=intervalle
        self.stopValue=False
        self.compteur=0
        self.fenetre=fenetre
        self.objet=objet
        
    def run(self):
        
        import time
        try :
            time.sleep(self.intervalle)
            self.fenetre.can.itemconfig(self.objet,image=self.images[self.compteur])
            if self.compteur<len(self.images)-1 :
                        
                self.compteur+=1
                
            else : self.compteur=0
            
            time.sleep(self.intervalle)
            self.fenetre.can.itemconfig(self.objet,image=self.images[self.compteur])
            if self.compteur<len(self.images)-1 :
                        
                self.compteur+=1
                
            else : self.compteur=0
            
            time.sleep(self.intervalle)
            self.fenetre.can.itemconfig(self.objet,image=self.images[self.compteur])
            if self.compteur<len(self.images)-1 :
                        
                self.compteur+=1
                
            else : self.compteur=0
            
            time.sleep(self.intervalle)
            self.fenetre.can.itemconfig(self.objet,image=self.images[self.compteur])
            if self.compteur<len(self.images)-1 :
                        
                self.compteur+=1
                
            else : self.compteur=0
                
        except RuntimeError : pass
        
    def stop(self):
        
        self.stopValue=True
        
class Debug :

    def __init__(self):

        pass


    def affType(self,value):

        value=type(value)

        if value==int :

            return "int."

        elif value==bool :

            return "boolean."

        elif value==float :

            return "float."

        elif value==str :

            return "string."

        elif value==list :

            return "list."

        elif value==dict :

            return "dict."
        
        elif value==tuple :
            
            return "tuple."

        else : return "Unknown / Error / None."


    def affVar(self,*variables):

        for i in range(len(variables)):

            print("value : ",variables[i])


    def affTypeVar(self,*variables):

        for i in range(len(variables)):

            print("type : ",Debug.affType("__local__",variables[i])," value : ",variables[i])


    def affReturnFonc(self,*variables):

        for i in range(len(variables)):

            print("La fonction retourne : ",Debug.affType("__local__",variables[i])," value : ",variables[i])


    def existFic(self,cheminFic=None):

        from os import listdir

        nomFic=self

        recherche=False

        fichiers=listdir(cheminFic)

        for i in range(len(fichiers)):

            if nomFic==fichiers[i] :

                recherche=True
                break

        return recherche

    def existRep(self,cheminRep):

        from os import listdir

        try :

            return bool(listdir(cheminRep))

        except (FileNotFoundError) :

            return False



