from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from app.downloader import download_audio
from app.transcriber import transcribe_audio
from app.summarizer import summarize_transcript
import uuid
import requests as http_requests
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

print("Supabase URL:", os.getenv("SUPABASE_URL"))
print("Supabase Key:", os.getenv("SUPABASE_KEY"))

# Initialize Supabase client
supabase: Client = create_client(
    supabase_url=os.getenv("SUPABASE_URL"),
    supabase_key=os.getenv("SUPABASE_KEY")
)

# Requests are limited per client IP.
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def index():
    return FileResponse("app/static/index.html")

# Register the error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class SummarizeRequest(BaseModel):
    yt_url: str

jobs = {}

def fetch_from_db(yt_url: str):
    response = supabase.table("summaries").select("*").eq("youtube_url", yt_url).execute()
    if response.data:
        return response.data[0]  # Return the first matching record
    return None

def save_to_db(yt_url: str, transcript: str, summary: str):
    supabase.table("summaries").insert({
        "youtube_url": yt_url,
        "transcript": transcript,   
        "summary": summary
    }).execute()


def run_pipeline(job_id: str, yt_url: str):
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["step"] = 1
        try:
            if existing := fetch_from_db(yt_url):
                jobs[job_id]["status"] = "completed"
                jobs[job_id]["step"] = 3
                jobs[job_id]["result"] = {
                    "summary": existing["summary"],
                    "transcript": existing["transcript"]
                }
                return
        except Exception:
            pass  # DB unavailable — continue with fresh processing
        jobs[job_id]["step"] = 1
        file_path = download_audio(yt_url)
        jobs[job_id]["step"] = 2
        transcript = transcribe_audio(file_path)
        jobs[job_id]["step"] = 3
        summary = summarize_transcript(transcript)
        try:
            save_to_db(yt_url, transcript, summary)
        except Exception:
            pass  # DB unavailable — still return result to user
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = {
            "summary": summary,
            "transcript": transcript
        }
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

@app.get("/video-info")
async def video_info(url: str):
    try:
        resp = http_requests.get(
            "https://www.youtube.com/oembed",
            params={"url": url, "format": "json"},
            timeout=6
        )
        resp.raise_for_status()
        data = resp.json()
        return {
            "title": data.get("title", ""),
            "channel": data.get("author_name", ""),
            "channel_url": data.get("author_url", ""),
        }
    except Exception:
        return {"title": "", "channel": "", "channel_url": ""}

@app.post("/summarize")
@limiter.limit("3/minute")
async def summarize(request: Request, body: SummarizeRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending", "result": None}
    background_tasks.add_task(run_pipeline, job_id, body.yt_url)
    return {"job_id": job_id}  # returns immediately

@app.get("/status/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]