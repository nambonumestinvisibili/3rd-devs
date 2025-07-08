import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

import OpenAIService
import json

with open("prompt.txt", "r") as file:
    prompt_text = file.read()

res = OpenAIService.OpenAiService.get_openai_completion(prompt_text, model="o4-mini")

with open("det-response.txt", "w") as response_file:
    response_file.write(json.dumps(res.to_dict(), indent=4))