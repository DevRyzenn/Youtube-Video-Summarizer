from whisper import load_model

model = load_model("base")

def transcribe_audio(file_path: str) -> str:
    """
    loads whisper (base) model 
    transcribes the audio file at file_path
    returns transcript as a plain string
    """
    transcript = model.transcribe(file_path)
    return transcript["text"]