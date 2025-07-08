import os

# Define the paths
source_dir = os.path.join(os.path.dirname(__file__), 'przesluchania', 'transcriptions')
output_file = os.path.join(os.path.dirname(__file__), 'intv-raw.txt')

# Ensure the source directory exists
if not os.path.exists(source_dir):
    raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")

# Open the output file for writing
with open(output_file, 'w', encoding='utf-8') as outfile:
    # Check if the source directory contains files
    files = os.listdir(source_dir)
    if not files:
        raise FileNotFoundError(f"No files found in the source directory '{source_dir}'.")
    
    # Iterate through all files in the source directory
    for filename in files:
        file_path = os.path.join(source_dir, filename)
        # Check if the file is a .txt file
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as infile:
                content = infile.read()
                # Write the filename and content to the output file
                outfile.write(f"Filename: {filename}\n")
                outfile.write(content + "\n\n")