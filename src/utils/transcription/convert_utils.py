# This file has utils for converting an audio or video file to MP3 format.

# Path: src/utils/convert_utils.py

import os
from pydub import AudioSegment
from werkzeug.utils import secure_filename
from tempfile import mkdtemp


def convert_to_mp3(file_storage):
    # Create a temporary directory to store files
    print("Hello world")

    temp_dir = mkdtemp()

    # Get a secure filename and save the uploaded file to the temp directory
    filename = secure_filename(file_storage.filename)
    filepath = os.path.join(temp_dir, filename)
    file_storage.save(filepath)

    # The output file path
    output_filename = os.path.splitext(filename)[0] + ".mp3"
    output_filepath = os.path.join(temp_dir, output_filename)

    print(output_filepath)

    # Convert the file to mp3
    try:


        # check to see if file is already mp3. If it is, skip conversion

        if filename.endswith(".mp3"):
            return filepath

        # # Load the file with pydub, which uses ffmpeg to decode
        # audio = AudioSegment.from_file(filepath)
        # # Export the file as an mp3
        # audio.export(output_filepath, format="mp3")
    except Exception as e:
        # Handle exceptions, such as the wrong file type
        print(f"An error occurred: {e}")

    # Return the path to the mp3 file
    return output_filepath


def convert_to_mp3_force(file_path):
    # Load the file with pydub, which uses ffmpeg to decode
    audio = AudioSegment.from_file(file_path)
    # The output file path
    output_filepath = os.path.splitext(file_path)[0] + ".mp3"
    # Export the file as an mp3
    audio.export(output_filepath, format="mp3")
    # Return the path to the mp3 file
    return output_filepath