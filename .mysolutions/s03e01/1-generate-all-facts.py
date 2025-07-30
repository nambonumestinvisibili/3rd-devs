import os
import json
from pathlib import Path

curr_dir = Path(__file__).parent

data_dir = curr_dir / 'data' / 'facts'
output_file = curr_dir / 'all-facts.json'
facts = []

for file_path in data_dir.iterdir():
  if file_path.is_file():
    content = file_path.read_text(encoding='utf-8')
    facts.append({'filename': file_path.name, 'text': content})

with open(output_file, 'w', encoding='utf-8') as out_f:
  json.dump(facts, out_f, ensure_ascii=False, indent=2)
