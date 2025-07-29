import base64
import openai
import globals

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def read_prompt(prompt_path):
    with open(prompt_path, "r") as file:
        prompt_text = file.read()
    return prompt_text

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
    
class PromptBuilder:
    def create_image_content(image_path):
        base64_image = encode_image(image_path)
        return {
            "type": "input_image",
            "image_url": f"data:image/jpeg;base64,{base64_image}"
        }
    
    def create_text_content(text):
        return {
            "type": "input_text",
            "text": text
        }
    
    def create_prompt(content):
        return [content]
    
    def create_user_message(content):
        return { "role": "user", "content": [*content] }



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