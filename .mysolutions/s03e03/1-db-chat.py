import os
from pathlib import Path
import sys
from uuid import uuid4

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from globals import aidevs_api_key
from OpenAIService import OpenAiService, HttpService
from VectorClient import VectorClient

def create_query(query: str):
  return {
    'task': 'database',
    'apikey':  aidevs_api_key,
    'query': query
  }

url = 'https://c3ntrala.ag3nts.org/apidb'
# res = HttpService.send_post_request(url, create_query('SHOW TABLES'))

# res = HttpService.send_post_request(url, create_query('SHOW CREATE TABLE users'))

prompt = """
  You are trying to iteratively discover an answer to the question below via executing SQL scripts.

  <goal>
    ID numbers of ACTIVE datacenters which are managed by managers who are currently on holidays (aka managers are unactive).
  </goal>

  <instructions>
    - Your response is only SQL script that I will execute. The script and response will be included here in the <history> tag.  
    - Discover database via 'SHOW TABLE' or 'SHOW CREATE TABLE tablename' for those tables that you feel might be important.
    - Based on that information, generate a SQL that will answer the <goal> question.
    - DO NOT return anything else than SQL script. 
    - SQL might be case-sensitive. 
  </instructions>

  <history>
    {_history}
  <history>
"""

history = []

def format_history(history):
  return list(map(lambda el: f"""
[Q]: [{el[0]}]
[A]: [{el[1]}]
------
""", history))

for _ in range(100):
  input('Press enter to allow next executions')

  iter_prompt = prompt.format(_history=format_history(history))
  print(iter_prompt)
  query = OpenAiService.get_openai_completion(iter_prompt)

  url = 'https://c3ntrala.ag3nts.org/apidb'
  response = HttpService.send_post_request(url, create_query(query))

  history.append((query, response))