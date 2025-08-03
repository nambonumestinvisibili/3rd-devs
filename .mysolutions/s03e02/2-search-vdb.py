import os
from pathlib import Path
import sys
from uuid import uuid4

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from OpenAIService import OpenAiService, HttpService
from VectorClient import VectorClient

question = 'W raporcie, z którego dnia znajduje się wzmianka o kradzieży prototypu broni?'

vc = VectorClient('aidevs-3x2')
embedding = vc.create_embedding(question)

rres = vc.search(embedding)
answer = rres.points[0].payload['date']

x = answer.replace("_", "-")
HttpService.send_report('wektory', x)