import logging
import os
from pathlib import Path
from typing import Optional

from moviepy.editor import AudioFileClip
from pytube import YouTube

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def download_and_convert_to_mp3(
    url: str, output_path: str = "output", filename: str = "test"
) -> Optional[tuple[str, str, str]]:
    """Downloads a YouTube video and converts it to an mp3 file.

    Args:
        url (str): The YouTube video URL
        output_path (str): The path to save the mp3 file (default: "output")
        filename (str): The name of the mp3 file (default: "test")

    Returns:
        Tuple[str, str, str]: A tuple containing the path to the mp3 file, the video title, and the video publish date.
    """
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        if audio_stream is None:
            logging.warning("No audio streams found")
            return None

        Path(output_path).mkdir(parents=True, exist_ok=True)

        mp3_file_path = os.path.join(output_path, filename + ".mp3")
        logging.info(f"Downloading started... {mp3_file_path}")

        downloaded_file_path = audio_stream.download(output_path)

        audio_clip = AudioFileClip(downloaded_file_path)
        audio_clip.write_audiofile(
            mp3_file_path, codec="libmp3lame", verbose=False, logger=None
        )
        audio_clip.close()

        if Path(downloaded_file_path).suffix != ".mp3":
            os.remove(downloaded_file_path)

        logging.info(
            f"Download and conversion successful. File saved at: {mp3_file_path}"
        )
        return (str(mp3_file_path), yt.title, yt.publish_date)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
