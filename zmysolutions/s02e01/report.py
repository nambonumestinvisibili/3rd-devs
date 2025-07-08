import os  
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

import OpenAIService
import json

# Read the content of prompt.txt
prompt_file_path = os.path.join(os.path.dirname(__file__), "det-response.txt")
with open(prompt_file_path, "r") as file:
    res_content = file.read()

# Convert the content to JSON
res_json = json.loads(res_content)

# Extract the required data
output_text = res_json["output"][1]["content"][0]["text"]
print(output_text)

resp = OpenAIService.HttpService.send_report("mp3", "Stanisława Łojasiewicza")
print(resp)