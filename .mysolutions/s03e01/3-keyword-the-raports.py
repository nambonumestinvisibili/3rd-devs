import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

# from OpenAIService import HttpService
import globals
from OpenAIService import OpenAiService, read_json, FileLocation

raport_data = read_json(__file__, '3-1-DATA.json')
facts_data = read_json(__file__, '2-all-facts-keywords-1.json')

prompt = f"""
You are an AI assistant that generates a report from the given data.
For each fact in the raport data, generate a list of keywords based on the facts in data.
For each fact in the raport data, loop through the facts data to find matching keywords. 
If you find a match, include the keywords that match the raport keywords in the report.
The filename has a meaning also - might be helpful in connecting sectors for example. 
Generate a new JSON object with the following structure:
{{
  "filename-01.txt" : "lista, słów, kluczowych 1",
  "filename-02.txt" : "lista, słów, kluczowych 2",
  ...
}}
<rules>
Keywords MUST BE in Polish
They must be in nominative case.
The keywords should be relevant to the content of the text.
The keywords should be separated by commas.
</rules>

<raport>
{raport_data}
</raport>

<facts>
{facts_data}
</facts>
"""
print(prompt)
OpenAiService.save_openai_completion_as_json(prompt, FileLocation(__file__, '3-answer.json'))