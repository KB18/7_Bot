from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

class TunHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.div = False
        self.cpt = 0
        self.Gcpt = 0
        self.nom_priere = []
        self.horaire_priere = []
        self.info_bonus = []
        self.alphab = "abcdefghijklmnopqrstuvwxyz"
        self.num = "0123456789"
    
    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for name, value in attrs:
                if name == "class":
                    self.div = True
                        

        

    def handle_data(self, data):
        if self.div == True and (self.une_lettre(data) or self.un_chiffre(data)):
            self.cpt+=1   
            print("Encountered data  :", data)
            if(self.cpt>3 and self.cpt<16):
                if self.cpt % 2 == 0:
                    self.horaire_priere.append(data)
                else:
                    self.nom_priere.append(data)
            else:
                self.info_bonus.append(data)
            
    def une_lettre(self, txt):
        for i in txt:
            for j in self.alphab:
                if i == j:
                    return True
        return False
    
    def un_chiffre(self, txt):
        for i in txt:
            for j in self.num:
                if i==j:
                    return True
        return False
        
    def resulte(self):
        return self.nom_priere, self.horaire_priere, self.info_bonus


def main():   
    parser = TunHTMLParser()
    url = "https://www.islamicfinder.org/prayer-widget/2996944/shafi/6/0/18.0/18.0"
    print('Ouverture de', url)

    response = urlopen(url)
    maintype = response.info().get_content_maintype()
    subtype = response.info().get_content_subtype()

    if maintype == 'text' and subtype == 'html':
        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8")
        parser.feed(htmlString)
    return parser.resulte()
