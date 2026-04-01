import yt_dlp
import os

SAVE_PATH = "audio/"

def ensure_dir_exists(path: str):
    os.makedirs(path, exist_ok=True)

def download_audio(youtube_url: str) -> str:
    """
    downloads audio using yt-dlp from a YouTube URL
    saves to local audio/ folder
    returns the file path as a string
    """
    ensure_dir_exists(SAVE_PATH)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': SAVE_PATH + '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        }],
        'restrictfilenames': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        file_path = ydl.prepare_filename(info)
        file_path = os.path.splitext(file_path)[0] + '.mp3'

    if os.path.exists(file_path):
        return file_path
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    
    return file_path
