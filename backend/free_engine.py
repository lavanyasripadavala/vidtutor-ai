import re
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def _split_sentences(text: str):
    text = re.sub(r"\s+", " ", text).strip()
    # simple sentence split
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if len(p.strip()) > 5]

def _top_k_sentences(context: str, query: str, k: int = 6):
    sents = _split_sentences(context)
    if not sents:
        return []

    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform(sents + [query])
    sims = cosine_similarity(X[:-1], X[-1])[:, 0]
    idxs = sims.argsort()[::-1][:k]
    return [sents[i] for i in idxs if sims[i] > 0.02]

def tutor_answer(context: str, question: str) -> str:
    hits = _top_k_sentences(context, question, k=7)
    if not hits:
        return "I could not find this in the video transcript. Try asking with different words."

    # “Explain like ChatGPT” formatting (still free)
    bullets = "\n".join([f"- {h}" for h in hits[:5]])
    return f"Here’s what the video says (from transcript):\n\n{bullets}\n\nIf you want, tell me which part you didn’t understand and I’ll simplify it."

def make_questions(context: str, n: int = 8):
    # pick top frequent content words and make template questions
    words = re.findall(r"[a-zA-Z]{4,}", context.lower())
    stop = set(["this","that","have","with","from","your","they","them","then","will","just","what","when","where","which","would","about"])
    words = [w for w in words if w not in stop]
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    keywords = sorted(freq, key=freq.get, reverse=True)[:12]

    templates = [
        "Explain the main idea of the video in simple words.",
        "What are the top 2 key points mentioned?",
        "What problem is the speaker trying to solve?",
        "What advice does the speaker give and why?",
        "Give one example mentioned (or implied) in the video.",
        "Summarize the video in 3 lines.",
    ]

    qs = []
    qs.extend(templates)

    for kw in keywords:
        qs.append(f"What does the video say about '{kw}'?")
        if len(qs) >= n:
            break

    return qs[:n]

def score_answer(context: str, question: str, user_text: str) -> dict:
    # reference = top transcript sentences relevant to the question
    ref = _top_k_sentences(context, question, k=6)
    ref_text = " ".join(ref)[:1200]

    if not user_text.strip():
        return {
            "score": 0,
            "correct": [],
            "missing": ["No answer detected."],
            "model_answer": ref_text or "Not found in transcript.",
            "followup_question": "Try answering again in 2–3 sentences.",
        }

    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform([ref_text, user_text])
    sim = cosine_similarity(X[0], X[1])[0][0] if ref_text else 0.0

    # score out of 10
    score = int(max(0, min(10, round(sim * 10))))

    correct = ref[:2] if ref else []
    missing = []
    if score <= 3:
        missing.append("Your answer is not matching the transcript closely. Mention the key points clearly.")
    if score <= 6:
        missing.append("Add more exact points from the video (2–3 points).")

    return {
        "score": score,
        "correct": correct,
        "missing": missing,
        "model_answer": ref_text or "Not found in transcript.",
        "followup_question": "Can you repeat the answer but include 2 clear points from the video?",
    }
