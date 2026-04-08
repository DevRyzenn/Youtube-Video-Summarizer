import yt_dlp
import os
import shutil

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

    # Discover ffmpeg portably: honour env var, then search PATH.
    # Only set ffmpeg_location when we can confirm the binaries exist.
    ffmpeg_location = os.environ.get("FFMPEG_LOCATION")
    if ffmpeg_location and not os.path.isdir(ffmpeg_location):
        ffmpeg_location = None
    if ffmpeg_location is None:
        ffmpeg_bin = shutil.which("ffmpeg")
        if ffmpeg_bin:
            ffmpeg_location = os.path.dirname(ffmpeg_bin)

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
    if ffmpeg_location:
        ydl_opts['ffmpeg_location'] = ffmpeg_location

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        file_path = ydl.prepare_filename(info)
        file_path = os.path.splitext(file_path)[0] + '.mp3'

    if os.path.exists(file_path):
        return file_path
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    
    return file_path
