import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

# from OpenAIService import HttpService
import globals
from OpenAIService import OpenAiService, read_json, FileLocation

data = read_json(__file__, 'all-facts.json')

prompt = f"""
You are an AI assistant that prepares all facts and keywords for the given data.
For all elements in a json list of facts, extract the keywords from the text and prepare a new json list with the following structure: 
{{
  "filename": "name of the file",
  "keywords": ["list", "of", "keywords"]
}}
<rules>
Keywords MUST BE in Polish
They must be in nominative case.
The keywords should be relevant to the content of the text.
The keywords should be separated by commas.
</rules>

<data>
{data}
</data>
"""
res = OpenAiService.save_openai_completion_as_json(
  prompt, 
  file_location=FileLocation(__file__, '2-all-facts-keywords-1.json'))

# res = OpenAiService.save_openai_completion_as_json(
#   'say hi as a json object. just one object with one property', 
#   file_location=FileLocation(__file__, '2-all-facts-keywords-1.json'))