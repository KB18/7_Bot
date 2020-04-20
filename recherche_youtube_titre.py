from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

class TunHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.div = False
        self.div_2 = False
        self.cpt = 0
        self.resulte = ""
        
    
    def handle_starttag(self, tag, attrs):
        if tag == "head":
            self.div = True

        if tag == "title":
            print("Encountered start tag  :", tag)
            self.div_2 = True




    def handle_endtag(self, tag):
        if tag == "head":
            self.div = False
        if tag == "title":
            self.div_2 = False
        

    def handle_data(self, data):
        if self.div == True:
            if self.div_2 == True:
                print("Encountered some data  :", data)
                self.resulte = data
    def resultePropre(self):
        chaine_reco = " - YouTube"
        longueur_reco = 11
        nb_lettre_reco = 0
        diff = len(self.resulte) - longueur_reco
        i = len(self.resulte) - 1
        j = len(chaine_reco) - 1

        stop_while = 500
        
        #recherche de le chaine a suppr
        
        if diff > 0:
            while i > diff:
                if(self.resulte[i] == chaine_reco[j]):
                    nb_lettre_reco += 1
                if (stop_while <= 0):
                    break
                i -= 1
                j -= 1
                stop_while -= 1
                
        #si trouver alors suppression
        if nb_lettre_reco == longueur_reco - 1 :
            print('RECONNUE')
            tmp = ""
            i = 0
            maxT = len(self.resulte) - longueur_reco + 1
            for i in range(maxT):
                tmp += self.resulte[i]
            self.resulte = tmp
        return self.resulte


def main(txt):   
    parser = TunHTMLParser()
    url = txt
    print('Ouverture de', url)

    response = urlopen(url)
    maintype = response.info().get_content_maintype()
    subtype = response.info().get_content_subtype()

    if maintype == 'text' and subtype == 'html':
        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8")
        parser.feed(htmlString)
    return parser.resultePropre()
