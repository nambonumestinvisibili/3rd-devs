import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from OpenAIService import HttpService
import globals

from openai import OpenAI
from OpenAIService import HttpService

txt = HttpService.send_get_request('https://c3ntrala.ag3nts.org/data/{apikey}/robotid.json')

txt = txt['description']

client = OpenAI(api_key=globals.openapi_api_key)

# result = { data: [{url: 'x'}]}
result = client.images.generate(
    model="dall-e-3",
    prompt=txt,
    size="1024x1024",
)

print(result.data[0].url)

HttpService.send_report('robotid', result.data[0].url)