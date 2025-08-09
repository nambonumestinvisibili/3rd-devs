import os
import sys
from pathlib import Path
import re
import time

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from globals import aidevs_api_key, models
from OpenAIService import OpenAiService, HttpService, read_file
import json

row = """
{{ 
  "messages": [
    {{ "role": "system", "content": "validate data" }},
    {{ "role": "user", "content": "{file_row_data}" }},
    {{ "role": "assistant", "content": "{file_row_result}" }}
  ]
}}
"""

correct = read_file(__file__, 'correct.txt')
incorrect = read_file(__file__, 'incorect.txt')

fine_tune_els = []
for r in correct.splitlines(): 
  populated_row = row.format(file_row_data=r, file_row_result="1")
  fine_tune_els.append(populated_row)
for r in incorrect.splitlines(): 
  populated_row = row.format(file_row_data=r, file_row_result="0")
  fine_tune_els.append(populated_row)

with open('to_tune.txt', 'w', encoding='utf-8') as f:
  for el in fine_tune_els:
    # Convert the string to a valid JSON object and dump as JSONL
    # Remove extra curly braces and parse as JSON
    el_json = json.loads(el.replace("{{", "{").replace("}}", "}"))
    f.write(json.dumps(el_json, ensure_ascii=False) + '\n')
