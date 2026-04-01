from fastapi import FastAPI
from pydantic import BaseModel
from app.downloader import download_audio
from app.transcriber import transcribe_audio
from app.summarizer import summarize_transcript

app = FastAPI()

class SummarizeRequest(BaseModel):
    yt_url: str

# TODO: this endpoint is synchronous and slow
# future improvement: run download + transcription as a background task
# and return a job_id immediately, then poll for results

@app.post("/summarize")
async def summarize(request: SummarizeRequest):
    file_path = download_audio(request.yt_url)
    transcript = transcribe_audio(file_path)
    summary = summarize_transcript(transcript)
    return {
        "summary": summary,
        "transcript": transcript
    }