import os
import whisper
import ssl 

ssl._create_default_https_context = ssl._create_unverified_context

def transcribe_audio_files(folder_path):
    # Load the Whisper model
    model = whisper.load_model("base")

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # Check if the file is an audio file
        if os.path.isfile(file_path) and file_name.lower().endswith(('.mp3', '.wav', '.m4a', '.flac')):
            print(f"Transcribing: {file_name}")
            
            # Transcribe the audio file
            result = model.transcribe(file_path)
            # result = { "text": "This is a dummy transcription for testing purposes." }  # Replace with actual transcription code
            # Save the transcription to a text file
            transcriptions_folder = os.path.join(folder_path, "transcriptions")
            os.makedirs(transcriptions_folder, exist_ok=True)
            output_file = os.path.join(transcriptions_folder, os.path.splitext(file_name)[0] + "_transcription.txt")
            
            print("Saving to " + output_file)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result["text"])
            
            print(f"Transcription saved to: {output_file}")

# Path to the 'przesluchania' folder
folder_path = os.path.join(os.path.dirname(__file__), "przesluchania")

# Call the function
transcribe_audio_files(folder_path)