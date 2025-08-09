import requests


# Przykładowe pytania do pliku tests.py:
questions = [
  'Samolot poleciał raz w prawo i dwa razy w dół', # skały
  # 'Dron poleciał dwa razy w dół i raz w prawo', # trawa
  # 'Dron poleciał dwa razy w prawo i raz w dół', # trawa
  # 'Dron poleciał w dół, w prawo, w dół', # trawa
  # 'Dron poleciał trzy razy w dół i trzy razy w prawo' # grota
]


def test_find_drone_location_api():
  url = 'http://localhost:8000/find-drone-location'
  for q in questions:
    response = requests.post(url, json={'query': q})
    print(f"Q: {q}\nA: {response.json()}\n")