# YouTube Video Summarizer

> Drop a YouTube link. Get a clean summary and full transcript — no sign-up, no fluff, just the takeaways.

A self-hosted web app that downloads audio from any public YouTube video, transcribes it with OpenAI Whisper, and summarises it using a Groq-hosted LLM — all within seconds.

---

## Features

- **Audio extraction** via yt-dlp (no browser, no cookies)
- **Speech-to-text** using OpenAI Whisper (runs locally)
- **AI summarisation** via Groq API (LLaMA)
- **Markdown-rendered summaries** — bold, lists, headings displayed correctly
- **Full transcript** displayed alongside the summary
- **Video metadata** — title and author fetched from YouTube oEmbed
- **Per-step pipeline UI** with real-time step sync and per-step timers
- **Result caching** via Supabase — same URL won't reprocess
- **Rate limiting** — 3 requests / minute per IP
- **Single-file frontend** served by FastAPI, no build toolchain

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| Audio download | yt-dlp |
| Transcription | OpenAI Whisper (local) |
| Summarisation | Groq API (LLaMA) |
| Caching | Supabase (PostgreSQL) |
| Rate limiting | SlowAPI |
| Frontend | Vanilla HTML/CSS/JS |
| Containerisation | Docker |

---

## Prerequisites

- Python 3.10+
- `ffmpeg` and `ffprobe` on your system PATH (auto-discovered; see [Install ffmpeg](#2-install-ffmpeg) section)
- A [Groq API key](https://console.groq.com/)
- A [Supabase](https://supabase.com/) project with a `summaries` table (optional — app works without it)

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/rabiazulfiqar1/yt-video-summarizer
cd yt-video-summarizer
```

### 2. Install ffmpeg

The app auto-discovers `ffmpeg` and `ffprobe` from your system PATH. Choose any method below that works for your OS:

```bash
# Linux (Debian/Ubuntu)
sudo apt-get install ffmpeg

# Linux (Fedora/RHEL)
sudo dnf install ffmpeg

# macOS (Homebrew — recommended)
brew install ffmpeg

# macOS (MacPorts)
sudo port install ffmpeg

# Windows (Chocolatey)
choco install ffmpeg

# Windows (Scoop)
scoop install ffmpeg

# Docker
# FFmpeg is pre-installed; no action needed.
```

**Optional:** Override ffmpeg location via environment variable (useful in Docker or CI):
```bash
export FFMPEG_LOCATION=/custom/path/to/ffmpeg/bin
python -m uvicorn app.main:app
```

### 3. Create a virtual environment

```bash
# Using uv (recommended)
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt

# Or standard pip
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_service_key
GROQ_API_KEY=your_groq_api_key
```

Supabase is optional — if the table doesn't exist the app will still summarise and return results, just without caching.

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

The app will auto-detect `ffmpeg` from your system PATH. No manual configuration needed.
```

Open [http://localhost:8000](http://localhost:8000)

---

## Docker

```bash
docker build -t yt-summarizer .
docker run -p 8000:8000 --env-file .env yt-summarizer
```

---

## Project Structure

```
app/
  main.py          # FastAPI app, routes, pipeline orchestration
  downloader.py    # yt-dlp audio download
  transcriber.py   # Whisper transcription
  summarizer.py    # Groq LLM summarisation
  static/
    index.html     # Complete frontend (HTML + CSS + JS)
tests/
  test_downloader.py
  test_summarizer.py
  test_transcriber.py
requirements.txt
Dockerfile
```

---

## API Reference

### `POST /summarize`
Submit a YouTube URL for processing. Returns a `job_id` immediately.

**Request body:**
```json
{ "yt_url": "https://www.youtube.com/watch?v=..." }
```

**Response:**
```json
{ "job_id": "uuid" }
```

Rate limited to **3 requests / minute per IP**.

---

### `GET /status/{job_id}`
Poll for job status.

**Response (processing):**
```json
{ "status": "processing", "step": 2, "result": null }
```

**Response (completed):**
```json
{
  "status": "completed",
  "step": 3,
  "result": {
    "summary": "...",
    "transcript": "..."
  }
}
```

Steps: `1` = downloading, `2` = transcribing, `3` = summarising.

---

### `GET /video-info?url=...`
Fetch video title and channel name via YouTube oEmbed.

**Response:**
```json
{
  "title": "Secrets of success in 8 words, 3 minutes",
  "channel": "TED",
  "channel_url": "https://www.youtube.com/@TED"
}
```
