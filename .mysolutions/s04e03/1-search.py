import json
import os
import sys
from pathlib import Path
import re
import time

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from globals import aidevs_api_key, models
from OpenAIService import OpenAiService, HttpService
import requests
from bs4 import BeautifulSoup

API_URL = 'https://c3ntrala.ag3nts.org/report'

url = "https://c3ntrala.ag3nts.org/data/{apikey}/softo.json"

questions = HttpService.send_get_request(url)
print(f"[DEBUG] Questions loaded: {questions}")

def html_to_markdown(html):
  soup = BeautifulSoup(html, "html.parser")
  for tag in soup(["script", "style"]):
    tag.decompose()
  text = soup.get_text(separator="\n")
  print(f"[DEBUG] Converted HTML to Markdown, length: {len(text)}")
  return text

def get_links(html, base_url):
  soup = BeautifulSoup(html, "html.parser")
  links = []
  for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.startswith("http"):
      links.append(href)
    elif href.startswith("/"):
      links.append(f"https://softo.ag3nts.org{href}")
  print(f"[DEBUG] Extracted {len(links)} links from page")
  return links

def ask_llm_if_answer(page_md, question, links):
  prompt = f"""
Twoje zadanie:
- Sprawdź, czy na tej stronie (poniżej w Markdown) znajduje się odpowiedź na zadane pytanie.
- Jeśli odpowiedź jest dostępna, zwróć ją w formacie: TAK:{{krótka i zwięzła odpowiedź}} (nie podawaj linków, tylko konkretną odpowiedź).
- Jeśli odpowiedzi nie ma, wybierz jeden najbardziej obiecujący link z listy (lub napisz BRAK jeśli żaden nie pasuje) w formacie: NIE:{{link lub BRAK}}.
- Nie odpowiadaj calym zdaniem, tylko tak krótko jak się da.
- Adres mailowy musi zawierać @. 

Pytanie: {question}

Dostępne linki:
{chr(10).join(f"{i+1}. {link}" for i, link in enumerate(links))}

<strona>
{page_md}
</strona>
"""
  response = OpenAiService.get_openai_completion(prompt, models.gpt41)
  print(f"[DEBUG] LLM response: {response}")
  return response

def search_for_answer(question):
  visited = set()
  url = "https://softo.ag3nts.org"
  for depth in range(10):  # Limit depth to avoid infinite loops
    print(f"[DEBUG] Visiting URL: {url} (depth {depth})")
    if url in visited:
      print("[DEBUG] URL already visited, breaking loop.")
      break
    visited.add(url)
    resp = requests.get(url)
    page_md = html_to_markdown(resp.text)
    links = get_links(resp.text, url)
    llm_response = ask_llm_if_answer(page_md, question, links)

    if "TAK" in llm_response.upper():
      answer = llm_response.split(":", 1)[1]
      print(f"[DEBUG] Found answer: {answer}")
      return answer if answer else llm_response

    elif "BRAK" in llm_response.upper():
      print("[DEBUG] LLM returned BRAK, no answer found.")
      return "Nie znaleziono odpowiedzi."
    elif "NIE" in llm_response.upper():
      url = llm_response.split(":", 1)[1].strip()
      print(f"[DEBUG] LLM suggested new URL: {url}")
  print("[DEBUG] Exceeded max depth or no answer found.")
  return "Nie znaleziono odpowiedzi."

answers = []
questions = list(questions.items())
print(questions)

for q in questions:
  print(f"[DEBUG] Searching for answer to question: {q}")
  answer = search_for_answer(q)
  answers.append({"question": q, "answer": answer})
  print()

#   break

# answer = search_for_answer(questions[0])
# print(f"[DEBUG] Final answer: {answer}")

print(answers)


