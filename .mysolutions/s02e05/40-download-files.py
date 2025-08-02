import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from OpenAIService import OpenAiService, HttpService, read_json, PromptBuilder
import requests
# import globals

# import whisper
# import ssl 
# import json

modals = read_json(__file__, "2-to-process.json")

data_dir = os.path.join(parent_dir, "data")
os.makedirs(data_dir, exist_ok=True)

for item in modals:
  url = item.get("url")
  if not url:
    continue
  filename = os.path.basename(url)
  file_path = os.path.join(data_dir, filename)
  try:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(file_path, "wb") as f:
      for chunk in response.iter_content(chunk_size=8192):
        if chunk:
          f.write(chunk)
    print(f"Downloaded {url} to {file_path}")
  except Exception as e:
    print(f"Failed to download {url}: {e}")