import pytest
from app.transcriber import transcribe_audio

def test_transcribe_audio_returns_string():
    file_path = "audio\Secrets_of_success_in_8_words_3_minutes_Richard_St._John.mp3"
    result = transcribe_audio(file_path)
    assert isinstance(result, str)

def test_transcribe_audio_nonexistent_file_raises_exception():
    file_path = "audio/nonexistent_file.mp3"
    with pytest.raises(Exception):
        transcribe_audio(file_path)