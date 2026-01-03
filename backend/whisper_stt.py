import os
import subprocess
import whisper

_model = None

def _get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")  # base = good speed/quality
    return _model

def _ensure_wav(input_path: str) -> str:
    """
    Streamlit audio_input gives wav in most cases, but sometimes it can be webm.
    We convert to wav safely using ffmpeg.
    """
    root, ext = os.path.splitext(input_path)
    ext = ext.lower()

    if ext == ".wav":
        return input_path

    out_wav = root + ".wav"
    cmd = ["ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", out_wav]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return out_wav

def transcribe_file(path: str) -> str:
    wav_path = _ensure_wav(path)
    model = _get_model()
    result = model.transcribe(wav_path)
    return (result.get("text") or "").strip()
