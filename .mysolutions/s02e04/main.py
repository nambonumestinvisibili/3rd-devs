import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

# from OpenAIService import HttpService
import globals

import whisper
import ssl 
import json

ssl._create_default_https_context = ssl._create_unverified_context

def process_audio():
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

  # Path to the 'mp3' folder inside 'data'
  folder_path = os.path.join(os.path.dirname(__file__), "data", "mp3")

  # Ensure the folder exists
  if not os.path.exists(folder_path):
      print(f"Audio folder not found: {folder_path}")
      return

  # Call the function
  transcribe_audio_files(folder_path)

data_dir = os.path.join(os.path.dirname(__file__), "data")

txt_files = []
png_files = []
mp3_files = []

for root, dirs, files in os.walk(data_dir):
  for file in files:
    if file.endswith(".txt"):
      txt_files.append(os.path.join(root, file))
    elif file.endswith(".png"):
      png_files.append(os.path.join(root, file))
    elif file.endswith(".mp3"):
      mp3_files.append(os.path.join(root, file))

# print(data_dir)
# print(png_files)


# process_audio()

# path = "C:\\programmingpractise\\aidevs\\3rd-devs\\.mysolutions\\s02e04"


# from OpenAIService import OpenAiService, PromptBuilder, read_prompt
# from globals import models
# import json

# prompt = read_prompt("image_prompt.txt")


# images_contents = [PromptBuilder.create_image_content(filename) for filename in png_files]
# messages = [
#   PromptBuilder.create_text_content(prompt),
#   *images_contents
# ]
# prompt = PromptBuilder.create_prompt(PromptBuilder.create_user_message(messages))
# print(prompt)
# response = OpenAiService.get_openai_completion(
#   prompt, models.gpt04mini)
# print(response.to_dict())

# # Save the response text to 'picture-summary.json'
# output_path = os.path.join(os.path.dirname(__file__), "picture-summary.json")
# with open(output_path, "w", encoding="utf-8") as f:
#     json.dump({"text": response.text}, f, ensure_ascii=False, indent=2)

# transcriptions_dir = os.path.join(os.path.dirname(__file__), "data", "transcriptions")
# json_output_dir = os.path.dirname(__file__) 

# if os.path.exists(transcriptions_dir):
#   summaries = []
#   for file in os.listdir(transcriptions_dir):
#     if file.endswith(".txt"):
#       txt_path = os.path.join(transcriptions_dir, file)
#       with open(txt_path, "r", encoding="utf-8") as f:
#         content = f.read()
#       json_obj = {
#         "filename": file,
#         "text": content
#       }
#       summaries.append(json_obj)

#   # Save the summaries to a JSON file
#   if summaries:
#     with open(json_output_dir + "\\transcriptions_summary.json", "w", encoding="utf-8") as f:
#       json.dump(summaries, f, ensure_ascii=False, indent=2)


# Read the 'transcriptions_summary.json' file
# transcriptions_summary_path = os.path.join(os.path.dirname(__file__), "transcriptions_summary.json")
# if os.path.exists(transcriptions_summary_path):
#   with open(transcriptions_summary_path, "r", encoding="utf-8") as f:
#     transcriptions_summary = json.load(f)
#   print("Loaded transcriptions summary:")
#   print(json.dumps(transcriptions_summary, ensure_ascii=False, indent=2))
# else:
#   print(f"File not found: {transcriptions_summary_path}")


# from OpenAIService import OpenAiService, PromptBuilder, read_prompt

# prompt = f"""
# <goal>
# Your goal is to categorize every filename text in the examples below into one of two categories.
# </goal>

# <instructions>
# There are two categories: PEOPLE and HARDWARE.
# If a text does not belong to the category, do not add it to any category.
# PEOPLE category includes notes about caught people or the traces of their presence.
# HARDWARE category includes hardware issues (but NOT SOFTWARE isses!)
# Data to classify is given below as json < filename: '', text: '' >.
# Response should be json: 

#   "PEOPLE": [list of filenames],
#   "HARDWARE": [list of filenames]

# </instructions>

# <data>
# {transcriptions_summary}
# </data>
# """
# from globals import models
# resp = OpenAiService.get_openai_completion(prompt, model=models.gpt04mini)
# print(resp.to_dict())

centrala_respo = {
  "people": sorted([
      "2024-11-12_report-00-sektor_C4.txt", 
      "2024-11-12_report-07-sektor_C4.txt",
      "2024-11-12_report-10-sektor-C1.mp3",
      # "2024-11-12_report-11-sektor-C2.mp3"
  ]),
  "hardware": sorted([
      "2024-11-12_report-13.png",
      "2024-11-12_report-15.png",
      "2024-11-12_report-17.png"
  ])
}

CENTRALA_R = {
      "task": "kategorie",
      "apikey": globals.aidevs_api_key,
      "answer": centrala_respo
}

from OpenAIService import HttpService
x = 'https://c3ntrala.ag3nts.org/report'
y = HttpService.send_post_request(x, CENTRALA_R)
print(y)