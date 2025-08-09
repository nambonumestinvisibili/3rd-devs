import json
import os
import sys
from pathlib import Path
import re
import time

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from globals import aidevs_api_key, models
from OpenAIService import OpenAiService, HttpService
import requests

prompt = """Jesteś nawigatorem, który świetnie zna teren i potrafi na podstawie mapy stwierdzić w jakim miejscu się znajduje dron.
Korsystasz z mapy i legendy i instrukcji drona gdzie poleciał.
Punktem startowym drona jest zawsze lewy górny róg - punkt startowy s.
Odpowiedz maksymalnie jednym lub dwoma słowami. 
Format odpowiedzi: {{
  "description": "dwa slowa"
}}

<instrukcja drona>
{drone_instruction}
</instrukcja drona

<mapa>
o t d c
t m t t 
t t k w
k k a g
</mapa>

<legenda>
o - start
t - trawa
d - drzewo
c - dom
m - młyn
k - skały
w - dwa drzewa
a - samochód
g - grota
</legenda>
"""

def find_location(query):
  print(query)
  airesponse = OpenAiService.get_openai_completion(prompt.format(drone_instruction=query))
  print(airesponse)
  return airesponse