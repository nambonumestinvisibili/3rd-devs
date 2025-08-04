import os
from pathlib import Path
import sys
from uuid import uuid4

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from globals import aidevs_api_key
from OpenAIService import OpenAiService, HttpService, read_file, read_json, FileLocation
from VectorClient import VectorClient
import json

extracted = read_json(__file__, '1-extracted.json')

people_queue = set(extracted['people'])
places_queue = set(extracted['cities'])

checked_names = set()
checked_cities = set()
found_barbara = None

def normalize(text):
  import unidecode
  return unidecode.unidecode(text.upper().strip())

def create_query(query: str):
  return {
    'apikey': aidevs_api_key,
    'query': query
  }

people_url = 'https://c3ntrala.ag3nts.org/people'
places_url = 'https://c3ntrala.ag3nts.org/places'

start_cities = set(normalize(city) for city in extracted['cities'])

def main():
  global found_barbara
  loop_count = 0
  while people_queue or places_queue:
    loop_count += 1
    print(f"\n--- Loop iteration {loop_count} ---")
    print(f"People queue: {people_queue}")
    print(f"Places queue: {places_queue}")
    print(f"Checked names: {checked_names}")
    print(f"Checked cities: {checked_cities}")
    print(f"Found Barbara: {found_barbara}")

    # Query people
    while people_queue:
      person = people_queue.pop()
      norm_person = normalize(person)
      print(f"Checking person: {person} (normalized: {norm_person})")
      if norm_person in checked_names:
        print(f"{norm_person} already checked.")
        continue
      checked_names.add(norm_person)
      response = HttpService.send_post_request(people_url, create_query(norm_person))
      r = json.loads(response)
      if r.get("code") != 0:
        print(f"Invalid response for person '{norm_person}': {r}")
        continue
      message = r["message"]
      if "RESTRICTED" in message:
        print(f"Access restricted for person '{norm_person}'.")
        continue
      message_list = message.split(" ") if isinstance(message, str) else []
      print(f"Response for person '{norm_person}': {message_list}")
      for place in message_list:
        norm_place = normalize(place)
        print(f"Adding place to queue: {place} (normalized: {norm_place})")
        if norm_place not in checked_cities:
          places_queue.add(norm_place)

    # Query places
    while places_queue:
      city = places_queue.pop()
      norm_city = normalize(city)
      print(f"Checking city: {city} (normalized: {norm_city})")
      if norm_city in checked_cities:
        print(f"{norm_city} already checked.")
        continue
      checked_cities.add(norm_city)
      response = HttpService.send_post_request(places_url, create_query(norm_city))
      r = json.loads(response)
      if r.get("code") != 0:
        print(f"Invalid response for city '{norm_city}': {r}")
        continue
      message = r["message"]
      if "RESTRICTED" in message or 'GLITCH' in message:
        print(f"Access restricted for city '{norm_city}'.")
        continue
      message_list = message.split(" ") if isinstance(message, str) else []
      print(f"Response for city '{norm_city}': {message_list}")
      for person in message_list:
        norm_person = normalize(person)
        print(f"Person found in city '{city}': {person} (normalized: {norm_person})")
        if norm_person == normalize("Barbara"):
          if normalize(city) not in start_cities:
            found_barbara = city
            print(f"Barbara found in: {city} (NEW city!)")
            break
          else:
            print(f"Barbara found in: {city}, but this city is in the starting note, skipping.")
        if norm_person not in checked_names:
          print(f"Adding person to queue: {person} (normalized: {norm_person})")
          people_queue.add(norm_person)
      if found_barbara:
        print("Breaking out of places loop, Barbara found.")
        break
    if found_barbara:
      print("Breaking out of main loop, Barbara found.")
      break

  # Report answer
  if found_barbara:
    answer_payload = {
      "task": "loop",
      "apikey": aidevs_api_key,
      "answer": normalize(found_barbara)
    }
    report_url = "https://c3ntrala.ag3nts.org/report"
    print(f"Reporting answer: {answer_payload}")
    resp = HttpService.send_post_request(report_url, answer_payload)
    print(f"Report response: {resp}")
  else:
    print("Barbara's current location could not be determined.")

main()
