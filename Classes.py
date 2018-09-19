
class Joueur():
    
    def __init__(self,nomJoueur,motDePasse):
        
        self.nomJoueur=nomJoueur
        self.motDePasse=motDePasse
        self.vitesseDeJeu=1
        self.stage=1
        self.etape=1
        self.warp=0
        self.money=0
        self.esprit=0
        self.espritNonDisponible=0
        self.modeLvlUp=1
        self.servants=[Servant("player", "DPC", 0, 1, 10, 10, 0.05, 0.05),
                       Servant("morrant", "DPS", 0, 1, 10, 10, 0.05, 0.05)]
        
        self.espritBonus={"DPC":100,
                          "DPS":100,
                          "money":100,
                          "critique":100,
                          "esprit":100}
        self.espritPrix={"DPC":1,
                         "DPS":1,
                         "money":1,
                         "critique":1,
                         "esprit":1}
        self.espritNiveau={"DPC":0,
                          "DPS":0,
                          "money":0,
                          "critique":0,
                          "esprit":0}
        self.espritLimiteNiveau={"DPC":0, 
                                "DPS":0,
                                "money":0,
                                "critique":100,
                                "esprit":0}
        
class Servant():
    
    def __init__(self,nom,status,bonus,niveau=1,degats=1,prix=5,tauxUpDegats=0.1,tauxUpPrix=0.1):
        
        self.nom=nom
        self.status=status
        self.bonus=bonus
        self.niveau=niveau
        self.degats=degats
        self.degatsBase=degats
        self.tauxUpDegats=tauxUpDegats
        self.prix=prix
        self.prixBase=prix
        self.tauxUpPrix=tauxUpPrix
        self.multiplicateur=1.001
        
class Monstre():
    
    def __init__(self):
        
        self.PV=10
        self.status="basique"
        self.gain=1
        self.gainEsprit=0
        

