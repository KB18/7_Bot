from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

class TunHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.div = False
        self.h3 = False
        self.a = False
        self.cpt = 0
        self.resulte = []
        
    def valide(self, url):
        succes = True
        lien_valide = "/watch?v="
        if(len(url)<len(lien_valide)):
            succes = False
        else:
            for i in range(len(lien_valide)):
                if url[i] != lien_valide[i]:
                    succes = False
        return succes
    
    def handle_starttag(self, tag, attrs):
            
        if tag == "div":
            self.div = True

        if tag == "h3":
            self.h3 = True

        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    #verification si lien valide
                    if self.valide(value):
                        #compteur pour prendre le deuxieme lien
                        self.cpt += 1

                        if self.cpt == 2:

                            self.a = True
                            print("------"+name+"------|------"+value+"------")
                            self.resulte.append(value)



    def handle_endtag(self, tag):
        pass
        

    def handle_data(self, data):
        if self.div == True:
            if self.h3 == True:
                if self.a == True:
                    print("Encountered some data  :", data)
                    self.resulte.append(data)
                    self.div = False
                    self.h3 = False
                    self.a = False

def formatClair(txt):
    #rendre compatible le texte avec le lien youtube de recherche
    xtx = ""
    cSpe = " "
    for c in range(len(txt)):
        if cSpe == txt[c]:
            xtx += "+"
        else:
            xtx += txt[c]
    return xtx

def main(txt):   
    parser = TunHTMLParser()
    txt = formatClair(txt)
    url = "https://www.youtube.com/results?search_query="+txt
    print('Ouverture de', url)

    response = urlopen(url)
    maintype = response.info().get_content_maintype()
    subtype = response.info().get_content_subtype()

    if maintype == 'text' and subtype == 'html':
        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8")
        parser.feed(htmlString)
    return parser.resulte[0], parser.resulte[1]
