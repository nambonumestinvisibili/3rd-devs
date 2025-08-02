
from bs4 import BeautifulSoup
import os
import sys
import json
from pathlib import Path

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from OpenAIService import read_file

file = read_file(__file__, "1-article.html")

if file:
  soup = BeautifulSoup(file, 'html.parser')

  img_tags = soup.find_all('img')
  images_objs = []
  image_contexts = []
  for img in img_tags:
    img_entity = img.get('src')
    if img_entity:
      # Resolve relative URLs if necessary
      if not img_entity.startswith(('http://', 'https://')):
        base_url = "https://c3ntrala.ag3nts.org/dane/"
        img_entity = f"{base_url}{img_entity.lstrip('/')}"
      # images_objs.append(img_entity)

      # Collect three previous siblings, the img tag, and three next siblings
      siblings = []
      prev = img
      for _ in range(3):
        prev = prev.find_previous_sibling()
        if prev:
          siblings.insert(0, prev)
        else:
           break
      siblings.append(img)
      next_ = img
      for _ in range(3):
        next_ = next_.find_next_sibling()
        if next_:
          siblings.append(next_)
        else:
           break
      # Merge their HTML/text
    
    context = ''.join(str(tag) for tag in siblings if tag)
    # image_contexts.append(context)
    images_objs.append({"type": 'image', "url": img_entity, "context": context})

  audio_tags = soup.find_all('audio') # Example for <audio> tags
  audio_objs = []
  for audio in audio_tags:
    # Get audio URL
    source_tag = audio.find('source')
    audio_entity = source_tag["src"] if source_tag and source_tag.has_attr("src") else None
    if audio_entity:
      if not audio_entity.startswith(('http://', 'https://')):
        base_url = "https://c3ntrala.ag3nts.org/dane/"
        audio_entity = f"{base_url}{audio_entity.lstrip('/')}"

      # Collect three previous siblings, the audio tag, and three next siblings
      siblings = []
      prev = audio
      for _ in range(3):
          prev = prev.find_previous_sibling()
          if prev:
              siblings.insert(0, prev)
          else:
           break
      siblings.append(audio)
      next_ = audio
      for _ in range(3):
          next_ = next_.find_next_sibling()
          if next_:
              siblings.append(next_)
          else:
              break
      # Merge their HTML/text
      context = ''.join(str(tag) for tag in siblings if tag)
      audio_objs.append({"type": 'audio', "url": audio_entity, "context": context})

  with open(Path(__file__).parent / "2-to-process.json", "w", encoding="utf-8") as toprocess:
    data = []
    for img_entity in images_objs:
        # print(img_entity)
        data.append({"type": "image", "url": img_entity["url"], "context": img_entity["context"]})
    for audio_entity in audio_objs:
        data.append({"type": "audio", "url": audio_entity["url"], "context": audio_entity["context"]})
    toprocess.write(json.dumps(data, ensure_ascii=False, indent=4))