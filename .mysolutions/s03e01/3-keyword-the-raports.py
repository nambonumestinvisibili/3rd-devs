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
Jesteś zaawansowanym asystentem AI, którego zadaniem jest generowanie listy słów kluczowych dla każdego wpisu raportu na podstawie danych raportowych oraz powiązanych faktów.

Instrukcje:
- Dla każdego wpisu w danych raportowych przeanalizuj treść i zidentyfikuj istotne słowa kluczowe.
- Dla każdej osoby, miejsca lub obiektu wspomnianego w raporcie, sprawdź w danych faktów, czy istnieją powiązane role, profesje, relacje, atrybuty lub inne istotne informacje (np. zawód, funkcja, powiązania rodzinne, specjalizacje, sektor, lokalizacja, powiązane wydarzenia). Jeśli tak, dodaj te informacje jako słowa kluczowe, nawet jeśli nie są bezpośrednio wymienione w raporcie.
- Jeśli raport opisuje wykrycie osoby lub obiektu, a fakty zawierają dodatkowe dane na ich temat (np. sektor, w którym znaleziono odciski palców, miejsce zatrzymania, powiązane osoby), dołącz te informacje jako słowa kluczowe.
- Jeśli w raporcie lub faktach nie ma bezpośredniej informacji o sektorze, lokalizacji lub innych szczegółach, ale można je wywnioskować z kontekstu (np. z nazwy pliku raportu lub metadanych), użyj tych informacji jako słów kluczowych.
- Łącz informacje z raportu, faktów oraz kontekstu (np. nazwa pliku, metadane), aby tworzyć zestaw słów kluczowych obejmujący zarówno pojęcia jawnie wymienione, jak i logicznie powiązane lub wynikające z wiedzy o osobach, miejscach czy obiektach.
- Uwzględniaj także synonimy i pojęcia ogólne (np. jeśli raport wspomina o "dzikiej zwierzynie", "leśnych zwierzętach" itp., użyj ogólnego słowa kluczowego "zwierzęta").
- Obsługuj drobne różnice w pisowni nazwisk i imion (np. "Kowaski" vs "Kowalski") jako odnoszące się do tej samej osoby.
- Słowa kluczowe powinny być możliwie najbardziej precyzyjne i wyczerpujące, ale tylko jeśli są logicznie powiązane z treścią raportu, faktami lub kontekstem.
- Wszystkie słowa kluczowe mają być w języku polskim, w mianowniku, oddzielone przecinkami.
- Nie dodawaj słów kluczowych niepowiązanych z treścią raportu, faktami ani kontekstem.

Format odpowiedzi:
Zwróć obiekt JSON, gdzie każdy klucz to nazwa pliku raportu, a wartość to ciąg słów kluczowych oddzielonych przecinkami. Przykład:
{{
  "filename-01.txt": "słowo1, słowo2, słowo3",
  "filename-02.txt": "słowo4, słowo5"
}}

<raport>
{raport_data}
</raport>

<fakty>
{facts_data}
</fakty>
"""
print(prompt)
OpenAiService.save_openai_completion_as_json(prompt, FileLocation(__file__, '3-answer.json'), model=globals.models.gpt41)