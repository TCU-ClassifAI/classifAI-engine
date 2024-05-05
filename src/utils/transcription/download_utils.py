import logging
import os
from pathlib import Path
from typing import Optional

from moviepy.editor import AudioFileClip
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError, VideoRegionBlocked, VideoUnavailable
import uuid

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_video_title(url: str) -> Optional[str]:
    """Get the title of a YouTube video.

    Args:
        url (str): The YouTube video URL

    Returns:
        Optional[str]: The title of the video
    """
    try:
        yt = YouTube(url)
        return yt.title
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None


def download_and_convert_to_mp3(
    url: str, output_path: str = "output", filename: str = str(uuid.uuid4())
) -> Optional[tuple[str, str, str]]:
    """Downloads a YouTube video and converts it to an mp3 file.

    Args:
        url (str): The YouTube video URL
        output_path (str): The path to save the mp3 file (default: "output")
        filename (str): The name of the mp3 file (default: "test")

    Returns:
        Tuple[str, str, str]: A tuple containing the path to the mp3 file, the video title, and the video publish date.

    Raises:
        Exception: An error occurred during the download and conversion process
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

        downloaded_file_path = audio_stream.download(
            output_path, filename=f"{filename}_temp"
        )

        logging.info(f"Downloaded file at: {downloaded_file_path}")

        audio_clip = AudioFileClip(downloaded_file_path)

        print(f"Converting to mp3... {mp3_file_path}")
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

    except AgeRestrictedError as e:
        logging.error(f"Age restricted video: {e}")
        raise AgeRestrictedError(
            "Unable to download age restricted video through pytube. Please try downloading the video manually."
        )
    except VideoRegionBlocked as e:
        logging.error(f"Video region blocked: {e}")
        raise VideoRegionBlocked(
            f"Unable to download video due to region restrictions."
        )
    except VideoUnavailable as e:
        logging.error(f"Video unavailable: {e}")
        raise VideoUnavailable(f"Unable to download video as it is unavailable.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        # print specific error type

        raise Exception(
            "An unknown error occurred while downloading and converting the video."
        )
