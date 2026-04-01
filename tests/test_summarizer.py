from app.summarizer import summarize_transcript

def test_summarize_transcript_returns_string():
    transcript = "AI is transforming the world in profound ways. It has the potential to revolutionize industries, improve healthcare, and enhance our daily lives. However, it also raises ethical concerns and challenges that we must address as a society."
    result = summarize_transcript(transcript)
    assert isinstance(result, str)
    assert len(result) > 0

def test_summarize_transcript_empty_input():
    transcript = ""
    result = summarize_transcript(transcript)
    assert isinstance(result, str)