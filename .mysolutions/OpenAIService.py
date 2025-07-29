
import openai
import globals

class OpenAiService:        
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
    


import requests

class HttpService:
    @staticmethod
    def send_post_request(url, data):
        try:
            response = requests.post(url, json=data, headers={"Content-Type": "application/json; charset=utf-8", 'accept': 'application/json'})
            # response.raise_for_status()  # Raise an HTTPError for bad responses
            response.encoding = 'utf-8'  # Ensure the response is decoded using UTF-8
            return response.text  # Return the response text, including any special characters
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    
    @staticmethod
    def send_get_request(url, params=None):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.text  # Return the text response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    @staticmethod
    def send_report(task_name, answer):
        body = {
        "task": task_name,
        "apikey": globals.aidevs_api_key,
        "answer": answer
        }
        post_url = f"https://c3ntrala.ag3nts.org/report"
        return HttpService.send_post_request(post_url, body)