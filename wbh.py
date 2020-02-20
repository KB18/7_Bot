import json
from urllib import request
from urllib.error import HTTPError

class wbh(object):
  """docstring for wbh"""
  def __init__(self, titre, description, type):
    if type == 0:
      WEBHOOK_URL = 'https://discordapp.com/api/webhooks/259331277071712256/Frc61BJyJILhhgx2s8ualMbuhQhBWJ2qgwoZJtFlvfnp1ekB9zAYvLI60e5es-FtNEs3'

      # La payload
      payload = {
        "embeds": [
          {
          "title": titre,
          "description": description,
          "color": 16777215
          }
        ]
      }

      # Les paramètres d'en-tête de la requête
      headers = {
          'Content-Type': 'application/json',
          'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
      }

      # Enfin on construit notre requête
      req = request.Request(url=WEBHOOK_URL,
                            data=json.dumps(payload).encode('utf-8'),
                            headers=headers,
                            method='POST')

      # Puis on l'émet !
      try:
          response = request.urlopen(req)
          print("sa fonctionne je pense ???")
          print(response.status)
          print(response.reason)
          print(response.headers)
      except HTTPError as e:
          print('ERROR')
          print(e.reason)
          print(e.hdrs)
          print(e.file.read())