import os
from pathlib import Path
import sys
from uuid import uuid4

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from OpenAIService import OpenAiService
from VectorClient import VectorClient

DATA_DIR = "data/weapons_tests/do-not-share"

client = OpenAiService.create_client()

embeddings_data = []

def map_to(filename):
  if filename.endswith(".txt"):
    date_part = filename.replace(".txt", "")
    file_path = os.path.join(DATA_DIR, filename)
    with open(file_path, "r", encoding="utf-8") as f:
      content = f.read()
    return (date_part, content)
  else:
    raise 'Error'

files = os.listdir(Path(__file__).parent / DATA_DIR)
before_points = list(map(lambda x: map_to(x), files))

vc = VectorClient('aidevs-3x2')
points = [{
    "id": uuid4(),
    "text": pt[1],
    "payload": {
      "date": pt[0],
      "text": pt[1]
    }} for pt in before_points ]
vc.upsert_many(points)