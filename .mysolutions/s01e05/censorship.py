import requests
import sys
import os

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

# Import global.py from the parent directory
import globals
import openai

def send_post_request(url, data):
    try:
        response = requests.post(url, json=data, headers={"Content-Type": "application/json; charset=utf-8", 'accept': 'application/json'})
        # response.raise_for_status()  # Raise an HTTPError for bad responses
        response.encoding = 'utf-8'  # Ensure the response is decoded using UTF-8
        return response.text  # Return the response text, including any special characters
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def send_get_request(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text  # Return the text response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def get_openai_completion(prompt, model="o4-mini", max_tokens=100, temperature=0.7):
    try:
        client = openai.OpenAI(
            api_key=globals.openapi_api_key
        )

        response = client.responses.create(
            model=model,
            input=prompt,
            # max_output_tokens=max_tokens,
            # temperature=temperature,
        )
        return response
    except Exception as e:
        print(f"An error occurred while getting OpenAI completion: {e}")

# Example usage
# apiKey = "aff1e95c-950e-4995-a153-e5bad44b1eae"
url = f"https://c3ntrala.ag3nts.org/data/{globals.aidevs_api_key}/cenzura.txt"
textToCensor = send_get_request(url)
print(textToCensor)

prompt = f"""
    You are a text censoring agent. Your task is to censor the following text according to the rules provided. The text to censor can be found in <text> tag.

    <rules>
    - The response needs to be in the same input as the input text, except for the parts that are to be censored. Do not repeat the tag and any special characters (like /n)
    - PII are to be censored. Name and surname should be replaced by CENZURA. Example: 'Jan Nowak' -> 'CENZURA'
    - Age should be replaced by CENZURA. Example: 'Jan Nowak ma 30 lat' -> 'CENZURA ma CENZURA lat'. 
    - Keep original format - for example keep 'lata' if they were in the og sentence. example: 'Jan Nowak ma 30 lata' -> 'CENZURA ma CENZURA lata'
    - The city should be replaced by CENZURA. Example: 'Jan Nowak lives in Warsaw' -> 'CENZURA lives in CENZURA'
    - The street and house number should be replaced by one word CENZURA. Example: 'Jan Nowak zyje na ul. 3 Maja 10' -> 'CENZURA zyje na ul. CENZURA'
    </rules>

    <text>
    {textToCensor}
    </text>
"""

censoredTextResponse = get_openai_completion(prompt)
print(censoredTextResponse)

chat_answer = censoredTextResponse.output_text
print("chat answer")
print(chat_answer)

# chat_answer = "Osoba podejrzana to CENZURA. Adres: CENZURA, CENZURA. Wiek: CENZURA lat."
body = {
    "task": "CENZURA",
    "apikey": globals.aidevs_api_key,
    "answer": chat_answer
    }
post_url = f"https://c3ntrala.ag3nts.org/report"
res = send_post_request(post_url, body)
print(res)