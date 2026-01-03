import os
import streamlit as st

from backend.ingest import load_video_knowledge
from backend.free_engine import tutor_answer, make_questions, score_answer
from backend.whisper_stt import transcribe_file
from backend.ui_css import inject_css

st.set_page_config(page_title="VidTutor AI", layout="wide")
inject_css(st)

# ---------- state ----------
defaults = {
    "context": "",
    "source": "",
    "mode": "Tutor Chat",
    "chat": [],                # list of {role, content}
    "history": [],             # list of video urls
    "qs": [],
    "q_idx": 0,
    "total_score": 0,
    "answered": 0,
    "last_result": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------- SIDEBAR (ChatGPT-like) ----------
st.sidebar.title("VidTutor AI")
st.sidebar.caption("FREE tutor + voice interview (no API limits)")

# history list
if st.session_state["history"]:
    st.sidebar.subheader("Video History")
    for i, u in enumerate(st.session_state["history"][-8:][::-1]):
        if st.sidebar.button(f"▶ {u[:28]}...", key=f"hist_{i}"):
            st.session_state["current_url"] = u

st.sidebar.divider()
st.session_state["mode"] = st.sidebar.radio("Mode", ["Tutor Chat", "Interview Voice"])

url = st.sidebar.text_input("Paste YouTube link", key="url_input")
load_btn = st.sidebar.button("Load Video", type="primary")

if load_btn:
    if not url:
        st.sidebar.error("Paste a YouTube link first.")
    else:
        status = st.sidebar.empty()
        status.info("Loading transcript (captions → else whisper)...")
        try:
            data = load_video_knowledge(url)
        except Exception as e:
            status.error(f"Failed: {e}")
            st.stop()

        st.session_state["context"] = data["context"]
        st.session_state["source"] = data["source"]
        st.session_state["chat"] = []
        st.session_state["qs"] = []
        st.session_state["q_idx"] = 0
        st.session_state["total_score"] = 0
        st.session_state["answered"] = 0
        st.session_state["last_result"] = None

        if url not in st.session_state["history"]:
            st.session_state["history"].append(url)

        status.success(f"Loaded ✅ ({data['source']})")

# ---------- HEADER ----------
c1, c2 = st.columns([3, 1])
with c1:
    st.title("VidTutor AI")
    st.caption(f"Source: **{st.session_state['source']}**  |  Chat-style tutor + Voice interview")
with c2:
    st.metric("Interview Score", f"{st.session_state['total_score']}", f"Answered: {st.session_state['answered']}")

if not st.session_state["context"]:
    st.info("Paste a YouTube link in the sidebar and click **Load Video**.")
    st.stop()

# ---------- Tutor Chat ----------
if st.session_state["mode"] == "Tutor Chat":
    st.subheader("Chat with the video (FREE)")

    # render chat
    for m in st.session_state["chat"]:
        role = m["role"]
        avatar = "You" if role == "user" else "AI"
        cls = "user" if role == "user" else "assistant"
        st.markdown(
            f"""
            <div class="chat-row {cls}">
              <div class="chat-avatar">{avatar}</div>
              <div class="chat-bubble">{m["content"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    msg = st.chat_input("Ask anything about this video...")
    if msg:
        st.session_state["chat"].append({"role": "user", "content": msg})

        with st.spinner("Thinking (FREE engine)..."):
            ans = tutor_answer(st.session_state["context"], msg)

        st.session_state["chat"].append({"role": "assistant", "content": ans})
        st.rerun()

# ---------- Interview Voice ----------
else:
    st.subheader("Interview (Voice) — Face-to-face style (FREE)")

    # Generate questions once
    if not st.session_state["qs"]:
        if st.button("Generate Interview Questions"):
            st.session_state["qs"] = make_questions(st.session_state["context"], n=8)
            st.session_state["q_idx"] = 0
            st.session_state["last_result"] = None
            st.success("Questions ready ✅")

    if not st.session_state["qs"]:
        st.info("Click **Generate Interview Questions** to start.")
        st.stop()

    idx = st.session_state["q_idx"]
    if idx >= len(st.session_state["qs"]):
        st.success("Interview Finished ✅")
        st.write(f"Final Score: **{st.session_state['total_score']}**")
        st.stop()

    question = st.session_state["qs"][idx]
    st.markdown(f"### Question {idx+1}")
    st.write(question)

    st.write("### 🎙️ Speak your answer")
    audio = st.audio_input("Record your answer")

    colA, colB = st.columns([1, 1])

    if audio is not None:
        os.makedirs("data/audio", exist_ok=True)
        ans_path = f"data/audio/answer_{idx}.wav"
        with open(ans_path, "wb") as f:
            f.write(audio.getvalue())

        st.success("Audio captured ✅ (Transcribing...)")

        try:
            text = transcribe_file(ans_path)
        except Exception as e:
            st.error(f"Transcription failed: {e}")
            st.stop()

        st.write("✅ Your answer (text):")
        st.text_area("", value=text, height=110)

        with colA:
            if st.button("Score Answer", type="primary"):
                r = score_answer(st.session_state["context"], question, text)
                st.session_state["last_result"] = r

                st.session_state["total_score"] += int(r.get("score", 0))
                st.session_state["answered"] += 1
                st.rerun()

        with colB:
            if st.button("Next Question ▶"):
                st.session_state["q_idx"] += 1
                st.session_state["last_result"] = None
                st.rerun()

    # show last result (so it does NOT “disappear”)
    if st.session_state["last_result"]:
        r = st.session_state["last_result"]
        st.markdown(f"## ✅ Score: {r.get('score',0)}/10")

        st.subheader("✅ Correct points")
        st.write(r.get("correct", []))

        st.subheader("❌ Missing points")
        st.write(r.get("missing", []))

        st.subheader("⭐ Model Answer (Perfect)")
        st.write(r.get("model_answer", ""))

        st.subheader("🔁 Follow-up Question")
        st.write(r.get("followup_question", ""))
