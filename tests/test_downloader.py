import pytest
import os
from app.downloader import download_audio

def test_download_audio_returns_string():
    url = "https://www.youtube.com/watch?v=Y6bbMQXQ180" 
    result = download_audio(url)
    assert isinstance(result, str)

def test_download_audio_file_exists():
    url = "https://www.youtube.com/watch?v=Y6bbMQXQ180"
    result = download_audio(url)
    assert os.path.exists(result) is True

def test_download_audio_bad_url_raises_exception():
    url = "https://youtube.com/watch?v=invalid123"
    with pytest.raises(Exception):
        download_audio(url)
