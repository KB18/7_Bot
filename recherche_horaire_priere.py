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
    
    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for name, value in attrs:
                if name == "class":
                    if value == "HBox":
                        self.div = True

        

    def handle_data(self, data):
        if self.div == True:
            self.cpt+=1
            if self.cpt > 3 and self.Gcpt < 6:
                if self.cpt == 5:
                    self.Gcpt += 1
                    self.cpt = 0
                    self.horaire_priere.append(data)
                if self.cpt == 4:
                    self.nom_priere.append(data)
                    
                #print("Encountered data  :", data)
        
    def resulte(self):
        return self.nom_priere, self.horaire_priere


def main():   
    parser = TunHTMLParser()
    url = "http://mosquee-lyon.org/Includes/horaires_de_priere.php"
    print('Ouverture de', url)

    response = urlopen(url)
    maintype = response.info().get_content_maintype()
    subtype = response.info().get_content_subtype()

    if maintype == 'text' and subtype == 'html':
        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8")
        parser.feed(htmlString)
    return parser.resulte()
print(main())
