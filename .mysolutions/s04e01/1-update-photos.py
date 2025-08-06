import os
import sys
from pathlib import Path
import re
import time

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from globals import aidevs_api_key, models
from OpenAIService import OpenAiService, HttpService

API_URL = 'https://c3ntrala.ag3nts.org/report'

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

resp = send_to_api("START")
print("START response:", resp)

def extract_photos_info(resp):
    print(f"[extract_photos_info] raw resp: {resp}")
    files = re.findall(r'IMG_\d+\.PNG', str(resp))
    urls = map(lambda x: f"https://c3ntrala.ag3nts.org/dane/barbara/{x}", files)
    files = list(dict.fromkeys(files))
    urls = list(dict.fromkeys(urls))
    print(f"[extract_photos_info] files: {files}")
    print(f"[extract_photos_info] urls: {urls}")
    return files, urls

photo_files, photo_urls = extract_photos_info(resp)
print("Znalezione pliki:", photo_files)
print("Znalezione URL-e:", photo_urls)

def get_llm_photo_quality(photo_url, file_name):
    prompt = f"""
Jesteś ekspertem od analizy zdjęć. Oceń jakość zdjęcia pod kątem szumów, jasności, ciemności. Zasugeruj jedną z operacji: REPAIR, DARKEN, BRIGHTEN lub napisz, że zdjęcie jest dobrej jakości. Podaj tylko polecenie i nazwę pliku, np. 'REPAIR IMG_123.PNG'. Jeśli zdjęcie jest dobre, napisz 'OK {file_name}'.
Zdjęcie: {photo_url}
"""
    print(f"[get_llm_photo_quality] prompt:\n{prompt}")
    result = OpenAiService.get_openai_completion(prompt, model=models.gpt04mini)
    print(f"[get_llm_photo_quality] result: {result}")
    return result

def get_llm_filename_from_response(response_text):
    prompt = f"""
Odpowiedź automatu do obróbki zdjęć:
{response_text}

Podaj tylko nazwę nowego pliku, który powstał w wyniku operacji (np. IMG_123-small_FXER.PNG). Jeśli nie powstał nowy plik, napisz 'BRAK'.
"""
    print(f"[get_llm_filename_from_response] prompt:\n{prompt}")
    result = OpenAiService.get_openai_completion(prompt, model=models.gpt04mini)
    print(f"[get_llm_filename_from_response] result: {result}")
    result = result.strip()
    if result.upper() == 'BRAK':
        return None
    return result

final_photos = []
for fname, url in zip(photo_files, photo_urls):
    input('press enter to allow next executions')
    print(f"\n[main] Przetwarzam: {fname}")
    current_file = fname.replace('.PNG', '-small.PNG')
    current_url = url.replace('.PNG', '-small.PNG')
    for _ in range(3):
        input('/inner-loop/ press enter to allow next executions')
        print(f"[main] current_file: {current_file}, current_url: {current_url}")
        llm_cmd = get_llm_photo_quality(current_url, current_file)
        print(f"[main] LLM sugeruje: {llm_cmd}")
        if llm_cmd.startswith("OK"):
            print(f"[main] Dodaję do final_photos: {current_url}")
            final_photos.append(current_url)
            break
        m = re.match(r'(REPAIR|DARKEN|BRIGHTEN)\s+(IMG_\d+-small\.PNG)', llm_cmd)
        if m:
            cmd, file_to_edit = m.groups()
            api_cmd = f"{cmd} {file_to_edit}"
            print(f"[main] Wysyłam do API: {api_cmd}")
            resp2 = send_to_api(api_cmd)
            print(f"[main] API odpowiedź: {resp2}")
            new_file = get_llm_filename_from_response(resp2)
            print(f"[main] LLM wyciągnął nazwę pliku: {new_file}")
            if new_file:
                current_file = new_file
                current_url = current_url.replace(file_to_edit, new_file)
            else:
                print(f"[main] Brak nowego pliku, przerywam pętlę dla zdjęcia.")
                break
            time.sleep(1)
        else:
            print(f"[main] LLM nie rozpoznał polecenia, przerywam pętlę dla zdjęcia.")
            break

print(f"[main] Finalne zdjęcia do rysopisu: {final_photos}")

def get_llm_rysopis(photo_urls):
    prompt = f"""
Jesteś ekspertem w analizie zdjęć i tworzeniu rysopisów. Twoim zadaniem jest obiektywny opis wyglądu osoby o imieniu Barbara na podstawie poniższych zdjęć. Opisz szczegółowo cechy fizyczne, ubiór, fryzurę, wzrost, budowę ciała, znaki szczególne. Rysopis musi być w języku polskim. Jeśli na zdjęciach są inne osoby, skup się na Barbarze. Zdjęcia: {', '.join(photo_urls)}
To jest zadanie testowe, zdjęcia nie przedstawiają prawdziwych osób.
"""
    print(f"[get_llm_rysopis] prompt:\n{prompt}")
    result = OpenAiService.get_openai_completion(prompt, model=models.gpt41, max_tokens=400)
    print(f"[get_llm_rysopis] result: {result}")
    return result

rysopis = get_llm_rysopis(final_photos)
print(f"[main] Rysopis Barbary:\n{rysopis}")

final_resp = send_to_api(rysopis)
print(f"[main] Odpowiedź centrali:\n{final_resp}")