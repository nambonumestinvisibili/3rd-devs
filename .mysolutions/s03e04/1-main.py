import os
from pathlib import Path
import sys
from uuid import uuid4

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from globals import aidevs_api_key
from OpenAIService import OpenAiService, HttpService, read_file, FileLocation
from VectorClient import VectorClient

note = read_file(__file__, '1-note.txt')

prompt = f"""
Read the following note and extract all the names of people and cities.
Response format: 
{{
  "people": ["name1", "name2", ...],
  "cities": ["city1", "city2", ...]
}}

<note>
{note}
</note>
"""
OpenAiService.save_openai_completion_as_json(prompt, file_location=FileLocation(__file__, '1-extracted.json'))