import json
import os
import sys
from pathlib import Path

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from OpenAIService import OpenAiService, read_file, read_json, PromptBuilder

tx = read_file(__file__, "3-article.md")
js = read_json(__file__, "4-translated-modals.json")

prompt = f"""Stwórz jeden plik markdown, który zawiera:
- Przetworzony tekst artykułu z pliku `3-article.md`.
- Opisy obrazów (zamiast samych obrazów) z pliku `4-translated modals`.
- Transkrypcje nagrań (zamiast plików dźwiękowych) z pliku `4-translated modals`.

Zintegruj wszystkie te elementy w logicznej kolejności, zachowując przejrzystość i czytelność dokumentu. Upewnij się, że każdy opis obrazu i transkrypcja nagrania są wyraźnie oznaczone i umieszczone w odpowiednich miejscach względem tekstu artykułu. Można je rozpoznać po nazwach plików.
Skróć plik w takim sposób, żeby wciąż zachowywał wszystkie informacje.

<4-translated-modals.md>
{tx}
</4-translated-modals.md>

<3-article.md>
{js}
</3-article.md>
"""


messages = [
  PromptBuilder.create_text_content(prompt),
]
prompt = PromptBuilder.create_prompt(PromptBuilder.create_user_message(messages))
print(prompt)
resptext = OpenAiService.get_openai_completion(prompt)
print(resptext)
output_path = Path(__file__).parent / "5-generated-one.md"

with open(output_path, "w", encoding="utf-8") as f:
  f.write(resptext)