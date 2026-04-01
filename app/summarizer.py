import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def summarize_transcript(transcript: str) -> str:
    """
    loads GROQ_API_KEY from .env
    calls Groq API with transcript as input
    returns summary as a plain string
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages = [
            {
                "role": "system",
                "content": "You are a video summarizer. Summarize the transcript clearly and concisely. Do not ask follow-up questions."
            },
            {
                "role": "user",
                "content": f"Summarize this transcript:\n\n{transcript}"
            }
        ]
    )

    summary = response.choices[0].message.content.strip()

    return summary
