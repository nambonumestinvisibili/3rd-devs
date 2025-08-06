import os
import sys
from pathlib import Path
import re
import time

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
API_URL = 'https://c3ntrala.ag3nts.org/report'

from globals import aidevs_api_key, models
from OpenAIService import OpenAiService, HttpService
def send_to_api(answer):
    payload = {
        "task": "photos",
        "apikey": aidevs_api_key,
        "answer": answer
    }
    print(f"[send_to_api] payload: {payload}")
    resp = HttpService.send_post_request(API_URL, payload)
    print(f"[send_to_api] response: {resp}")
    return resp

prompt = """
Jesteś ekspertem w analizie zdjęć i tworzeniu rysopisów. Twoim zadaniem 
jest obiektywny opis wyglądu osoby o imieniu Barbara na podstawie poniższych zdjęć. Opisz szczegółowo cechy fizyczne, ubiór, fryzurę, wzrost, budowę ciała, znaki szczególne. Rysopis musi być w języku polskim. Jeśli na zdjęciach są inne osoby, skup się na Barbarze. 
Odpowiedz też na pytanie:
Gdzie znajduje się tatuaż Barbary?
Jaki kolor włosów ma Barbara?
Co takiego ma charakterystycznego w swoim wyglądzie?
Zdjęcia: https://c3ntrala.ag3nts.org/dane/barbara/IMG_559-small.PNG, https://c3ntrala.ag3nts.org/dane/barbara/IMG_1410_FXER.PNG, https://c3ntrala.ag3nts.org/dane/barbara/IMG_1443-small.PNG, https://c3ntrala.ag3nts.org/dane/barbara/IMG_1444-small.PNG
"""

result = OpenAiService.get_openai_completion(prompt, model=models.gpt41, max_tokens=400)

final_resp = send_to_api(result)
print(f"[main] Odpowiedź centrali:\n{final_resp}")