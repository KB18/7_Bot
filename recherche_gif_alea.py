from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
from urllib.error import HTTPError
from random import randrange
'''
auteur : KARIM
version : 1.0
desc : recherche et renvoie un gif associer a un mot rentrer en parm choisie aleatoirement dans le site de gif tenor
'''


class GifAleaChercheur(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.div = False
        self.result = []
        self.cpt_result = 0
        
    def commence_par(self, txt, mot):
        succes = True
        if(len(txt)<len(mot)):
            succes = False
        else:
            for i in range(len(mot)):
                if txt[i] != mot[i]:
                    succes = False
        return succes

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for name, value in attrs:
                if name == "class" and value == "Gif ":
                    self.div = True

        if tag == "img" and self.div == True:
            for name, value in attrs:
                if name == "src":
                    debut = "https://media.tenor.com/images/"
                    if self.commence_par(value, debut):
                        self.result.append(value)
                        self.cpt_result += 1
                        
    def gif(self):
        if self.result != [] and self.cpt_result != 0:
            print("gifs trouver")
            nb_alea = randrange(0, self.cpt_result - 1)
            return self.result[nb_alea]
        elif self.result != [] and self.cpt_result == 1:
            return self.result[0]
        else:
            msg_err = "gifs introuvable"
            print(msg_err)
            return msg_err

def formatClair(txt):
    #rendre compatible le texte avec le lien
    xtx = ""
    cSpe = " "
    for c in range(len(txt)):
        if cSpe == txt[c]:
            xtx += "-"
        else:
            xtx += txt[c]
    return xtx

def main(mot:str):
    parser = GifAleaChercheur()
    url="https://tenor.com/search/"+formatClair(mot)+"-gifs"
    print('Ouverture de', url)
    try:
        response = urlopen(url)
        maintype = response.info().get_content_maintype()
        subtype = response.info().get_content_subtype()

        if maintype == 'text' and subtype == 'html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            parser.feed(htmlString)
    except HTTPError:
        print('ahhhhhh pas trouver')
    return parser.gif()
    
#print(main(input('le mot : ')))
