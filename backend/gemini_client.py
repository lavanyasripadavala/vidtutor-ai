import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing in .env")

_client = genai.Client(api_key=API_KEY)

def llm(prompt: str, model: str = MODEL, retries: int = 3) -> str:
    last_err = None
    for _ in range(retries):
        try:
            r = _client.models.generate_content(model=model, contents=prompt)
            return (r.text or "").strip()
        except Exception as e:
            last_err = e
            msg = str(e)

            # Handle Gemini rate limit (429)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                time.sleep(3)  # small wait
                continue

            break

    raise RuntimeError(f"Gemini failed: {last_err}")
