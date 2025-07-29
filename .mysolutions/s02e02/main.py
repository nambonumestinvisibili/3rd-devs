import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from OpenAIService import OpenAiService, PromptBuilder, read_prompt
from globals import models 

path = "C:\\programmingpractise\\aidevs\\3rd-devs\\.mysolutions\\s02e02"

filenames = [
  "1.jpg",
  "2.jpg",
  "3.jpg",
  "4.jpg",
]

prompt = read_prompt("prompt.txt")

mapped_filenames = list(map(lambda x: path + "\\" + x, filenames))
images_contents = [PromptBuilder.create_image_content(filename) for filename in mapped_filenames ]
messages = [
  PromptBuilder.create_text_content(prompt),
  *images_contents
]
prompt = PromptBuilder.create_prompt(PromptBuilder.create_user_message(messages))

response = OpenAiService.get_openai_completion(
  prompt, models.gpt04mini)
print(response.to_dict())