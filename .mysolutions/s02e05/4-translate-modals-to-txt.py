import json
import os
import sys
from pathlib import Path
import whisper

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from OpenAIService import OpenAiService, HttpService, read_json, PromptBuilder
# import globals

# import whisper
# import ssl 
# import json

modals = read_json(__file__, "2-to-process.json")

def translate_modal_to_txt(modal):
  if modal['type'] == 'image':
    return translate_image(modal['url'], modal['context'])
  elif modal['type'] == 'audio':
    return translate_audio(modal['url'])

def translate_image(url, context):
  image_name = url.split('/')[-1]
  image_path = Path(__file__).parent / "data" / image_name
  prompt = f"""
  Translate the following image into text. 
  If you feel that the context found in <context> is important, you can use it in the description of the image.
  Be aware that the html tags are not important. 

  <context>
  {context}
  </context>
  """
  messages = [
    PromptBuilder.create_text_content(prompt),
    PromptBuilder.create_image_content(image_path) 
  ]
  prompt = PromptBuilder.create_prompt(PromptBuilder.create_user_message(messages))
  print(prompt)
  resptext = OpenAiService.get_openai_completion(prompt)
  return { "url": url, "text": resptext }

def translate_audio(url):
  audio_name = url.split('/')[-1]

  transcriptions = transcribe_audio_files(Path(__file__).parent / "data")

  return { "url": url, "text": transcriptions }
  # messages = [
  #   PromptBuilder.create_text_content(prompt),
  #   PromptBuilder.create_audio_content(url)
  # ]
  # prompt = PromptBuilder.create_prompt(PromptBuilder.create_user_message(messages))
  # return OpenAiService.get_openai_completion(prompt)

def transcribe_audio_files(folder_path):
    # Load the Whisper model
    model = whisper.load_model("base")

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        print(file_path)
        # Check if the file is an audio file
        if os.path.isfile(file_path) and file_name.lower().endswith(('.mp3', '.wav', '.m4a', '.flac')):
            print(f"Transcribing: {file_path}")
            
            # Transcribe the audio file
            result = model.transcribe(file_path)

            transcriptions_folder = os.path.join(os.path.dirname(folder_path), "transcriptions")
            os.makedirs(transcriptions_folder, exist_ok=True)
            output_file = os.path.join(transcriptions_folder, os.path.splitext(file_name)[0] + ".txt")
            
            print("Saving to " + output_file)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result["text"])
            
            print(f"Transcription saved to: {output_file}")
            return result['text']


translate_modal_to_txt(modals[-1])

js = list(map(lambda x: translate_modal_to_txt(x), modals))

with open(Path(__file__).parent / "4-translated-modals.json", "w", encoding="utf-8") as f:
  json.dump(js, f, ensure_ascii=False, indent=2)
