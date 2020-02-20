class Vote:
    cpt_vote = 0

    def __init__(self, titre):
        self.titre = titre
        self.id_vote = int(Vote.cpt_vote) + 0
        self.nb_vote = 0
        self.nb_oui = 0
        self.nb_non = 0
        self.tab_votant = []
        Vote.cpt_vote += 1
    '''Getter et mutateur'''
    def get_Nb_oui(self):
        return self.nb_oui
    def get_Nb_non(self):
        return self.nb_non
    def get_Nb_vote(self):
        return self.nb_vote
    def get_Titre(self):
        return self.titre
    def get_IdVote(self):
        return self.id_vote

    def set_Nb_oui(self, nb):
        self.nb_oui = int(nb)

    def set_Nb_non(self, nb):
        self.nb_non = int(nb)
    
    ''' fonction de la classe '''

    def addOui(self):
        self.nb_vote+=1
        self.nb_oui+=1

    def addNon(self):
        self.nb_vote+=1
        self.nb_non+=1

    def aDejaVoter(self, electeur):
        etat = False
        for i in self.tab_votant:
            if(electeur == i):
                etat = True
        return etat

    def ajtVotant(self, votant):
        self.tab_votant.append(str(votant))

    def getVotant(self):
        for i in self.tab_votant:
            print(i)
    
    def closeVote(self):
        La_fin = "LE VOTE n° "+str(self.get_IdVote())+" EST FINI VOICI LES RESULTATS"
        La_fin +=" \nNOMBRE DE VOTANT : "+str(self.get_Nb_vote())
        La_fin +="\nNOMBRE DE OUI :"+str(self.get_Nb_oui())
        La_fin +="\nNOMBRE DE NON :"+str(self.get_Nb_non())
        return str(La_fin)