import os
import sys
import json
from pathlib import Path

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from OpenAIService import HttpService, OpenAiService, read_file

knowledge = read_file(__file__, "5-generated-one.md")

url = 'https://c3ntrala.ag3nts.org/data/{apikey}/arxiv.txt'
questions = HttpService.send_get_request(url)

prompt = f"""
Na podstawie ponizszego tekstu w <knowledge> odpowiedz na pytania w <questions>.
Niech odpowiedzi będą zwięzłe (maksymalnie 1zdaniowe).
Format odpowiedzi:
{{
  "01": "Odpowiedź na pytanie 01",
  "02": "Odpowiedź na pytanie 02",
  ...
  "NR_PYTANIA": "Odpowiedź na pytanie NR_PYTANIA"
}}
<knowledge>
{knowledge}
</knowledge>  

<questions>
{questions}
</questions>
"""

# rt = OpenAiService.get_openai_completion(prompt)
# print(rt)

rt = {
  "01": "Użyto truskawki.",
  "02": "Fotografia wykonana była na Rynku Głównym w Krakowie.",
  "03": "Chciał znaleźć hotel.",
  "04": "Zostały pozostawione resztki pizzy z ananasem.",
  "05": "Litery BNW pochodzą od Brave New World."
}

task_resp = HttpService.send_report("arxiv", rt)
print(task_resp)