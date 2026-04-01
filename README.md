# YT Video Summarizer

Paste a YouTube URL, get an AI-generated summary back.

## Tech Stack
- FastAPI
- OpenAI Whisper
- yt-dlp  
- Groq (LLaMA)
- Docker

## Setup

1. Clone the repo
   git clone https://github.com/rabiazulfiqar1/yt-video-summarizer

2. Create virtual environment
   python -m venv .venv
   .venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Create .env file
   GROQ_API_KEY=your_key_here

5. Run the app
   uvicorn app.main:app --reload

6. Open Swagger UI
   http://localhost:8000/docs