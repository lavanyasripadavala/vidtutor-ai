

````md
# 🎥 VidTutor AI

VidTutor AI is an AI-powered learning platform that transforms any YouTube video into an interactive tutor and real-time interview coach. Users can chat with video content, practice interview questions using voice, and receive automatic scoring and feedback — all without relying on paid AI APIs.



## 🚀 Features

- 🔗 Paste any YouTube link and extract knowledge automatically  
- 💬 Tutor Chat — Ask questions and get answers from the video content  
- 🎙️ Voice Interview Mode — Practice interviews by speaking, not typing  
- 🧠 Automatic question generation, scoring, feedback, and model answers  
- 🆓 Fully offline & free AI engine (no API limits)  
- ⚡ Transcript caching for fast performance  


## 🧰 Tech Stack

| Layer | Technology |
|------|-----------|
Frontend | Streamlit  
Speech Processing | Whisper, FFmpeg  
ML Engine | TF-IDF, Cosine Similarity (scikit-learn)  
Video Processing | yt-dlp  
Deployment | Docker, HuggingFace Spaces  


## 🏗️ How It Works

1. User pastes a YouTube link  
2. App extracts transcript from captions or transcribes audio using Whisper  
3. Tutor Mode: Chat with the video content  
4. Interview Mode: Speak answers → get score, feedback & model answers  
5. Results improve learning and interview performance  


## 🖥️ Run Locally

```bash
git clone https://github.com/yourusername/vidtutor-ai
cd vidtutor-ai
pip install -r requirements.txt
streamlit run app.py
````

---

## 🌍 Live Demo

👉 (link)

---

## 📌 Why VidTutor AI?

VidTutor AI turns passive video watching into active learning and interview preparation by combining AI, speech recognition, and machine learning in one seamless platform.


