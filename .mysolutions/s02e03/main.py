import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from OpenAIService import HttpService
import globals

x = f'https://centrala.ag3nts.org/data/{globals.aidevs_api_key}/robotid.json'
y = HttpService.send_get_request()

print(y)