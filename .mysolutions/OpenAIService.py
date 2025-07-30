import base64
import openai
import globals
import json 
from pathlib import Path

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def read_prompt(prompt_path):
    with open(prompt_path, "r") as file:
        prompt_text = file.read()
    return prompt_text

def read_json(json_path_of_calling_file, json_filename):
    loc = Path(json_path_of_calling_file).parent / json_filename
    print(loc)
    with open(loc, "r", encoding='utf-8') as file:
        return json.load(file)

class FileLocation:
    def __init__(self, magic_file, filename):
        self.file_path = Path(magic_file).parent / filename

    def get_parent_directory(self):
        return self.file_path.parent
    
    def get_absolute_path(self):
        return self.file_path.resolve()
    
    def get_filename(self):
        return self.file_path.name
    
    def get_extension(self):
        return self.file_path.suffix

class OpenAiService:    
    def get_openai_completion(prompt, model="o4-mini", max_tokens=100, temperature=0.7) -> str:
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

            print(json.dumps(json.loads(response.json()), indent=2))
            return response.output_text
        
        except openai.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except openai.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except openai.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
        except Exception as e:
            print(f"An error occurred while getting OpenAI completion: {e}")

    def save_openai_completion_as_json(prompt, file_location: FileLocation, model="o4-mini", max_tokens=100, temperature=0.7):
        try:
            response_text = OpenAiService.get_openai_completion(prompt, model, max_tokens, temperature)

            json_data = json.loads(response_text)

            if response_text:
                with open(file_location.get_absolute_path(), 'w', encoding='utf-8') as out_f:
                    json.dump(json_data, out_f, ensure_ascii=False, indent=2)
            else:
                print("No response received from OpenAI.")
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
    
    def create_audio_content(text):
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
            print(response.text)
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
        print('Sending raport....')
        return HttpService.send_post_request(post_url, body)