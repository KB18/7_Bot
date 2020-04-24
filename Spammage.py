from embedEnvoi import envoi
import asyncio
from time import sleep
from threading import Thread

class Spammage:
    titre = "Spammage"

    def __init__(self, spammeur, spammer):
        self.spammeur = spammeur
        self.spammer = spammer
        self.actif = True
        self.thread = None

    async def spamMSG(self, ctx):
        while self.actif:
            await envoi(ctx, titre=Spammage.titre, texte=self.spammer, auteur=self.spammeur, desti="spam")
            sleep(2)


    async def lancement(self, ctx):
        self.thread = Thread(target=self.spamMSG, args=ctx)

    def stop(self):
        self.thread.join()
        self.thread = None