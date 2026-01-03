import os
import hashlib
from yt_dlp import YoutubeDL
import whisper

CACHE_DIR = os.path.join("data", "cache")
AUDIO_DIR = os.path.join("data", "audio")

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

_whisper_model = None

def _get_whisper():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model("base")
    return _whisper_model

def _key(url: str) -> str:
    return hashlib.md5(url.encode("utf-8")).hexdigest()

def _save_cache(url: str, text: str, source: str):
    k = _key(url)
    with open(os.path.join(CACHE_DIR, f"{k}.txt"), "w", encoding="utf-8") as f:
        f.write(text)
    with open(os.path.join(CACHE_DIR, f"{k}.meta"), "w", encoding="utf-8") as f:
        f.write(source)

def _load_cache(url: str):
    k = _key(url)
    txt = os.path.join(CACHE_DIR, f"{k}.txt")
    meta = os.path.join(CACHE_DIR, f"{k}.meta")
    if os.path.exists(txt) and os.path.exists(meta):
        return open(txt, "r", encoding="utf-8").read(), open(meta, "r", encoding="utf-8").read()
    return None, None

def _get_captions_vtt(url: str) -> str | None:
    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "vtt",
        "quiet": True,
        "no_warnings": True,
        "outtmpl": os.path.join(CACHE_DIR, "captions.%(ext)s"),
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # find newest vtt
        for f in os.listdir(CACHE_DIR):
            if f.startswith("captions") and f.endswith(".vtt"):
                with open(os.path.join(CACHE_DIR, f), "r", encoding="utf-8", errors="ignore") as fp:
                    return fp.read()
        return None
    except Exception:
        return None

def _vtt_to_text(vtt: str) -> str:
    lines = []
    for line in vtt.splitlines():
        line = line.strip()
        if not line or line.startswith("WEBVTT") or "-->" in line:
            continue
        lines.append(line)
    return " ".join(lines)

def _download_audio_mp3(url: str) -> str:
    outtmpl = os.path.join(AUDIO_DIR, "yt_audio.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True,
        "no_warnings": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return os.path.join(AUDIO_DIR, "yt_audio.mp3")

def load_video_knowledge(url: str) -> dict:
    cached_text, cached_src = _load_cache(url)
    if cached_text:
        return {"context": cached_text, "source": f"cache ({cached_src})"}

    vtt = _get_captions_vtt(url)
    if vtt:
        text = _vtt_to_text(vtt)
        _save_cache(url, text, "captions")
        return {"context": text, "source": "captions"}

    # fallback: whisper
    mp3 = _download_audio_mp3(url)
    model = _get_whisper()
    result = model.transcribe(mp3)
    text = (result.get("text") or "").strip()
    _save_cache(url, text, "whisper")
    return {"context": text, "source": "whisper"}
