🎥 VidTutor AI

VidTutor AI is an AI-powered learning platform that transforms any YouTube video into an interactive tutor and real-time interview coach. Users can chat with the video content, practice interview questions using voice, and receive automatic scoring and feedback — all without relying on paid AI APIs.

🚀 Features

🔗 Paste any YouTube link and extract knowledge automatically

💬 Tutor Chat — Ask questions and get answers from the video content

🎙️ Voice Interview Mode — Practice interviews by speaking, not typing

🧠 Automatic question generation, scoring, feedback, and model answers

🆓 Fully offline & free AI engine (no OpenAI/Gemini limits)

⚡ Caching for fast performance on repeated videos

🧰 Tech Stack

Frontend: Streamlit

Speech Processing: Whisper + FFmpeg

ML Engine: TF-IDF, Cosine Similarity (scikit-learn)

Video Processing: yt-dlp

Deployment: Docker + HuggingFace Spaces

🏗️ How It Works

User pastes a YouTube link

App extracts transcript from captions or transcribes audio using Whisper

Tutor mode allows chatting with the video content

Interview mode asks questions, records voice answers, transcribes them, and evaluates responses

App generates score, feedback, missing points, and model answers

🖥️ Run Locally
git clone https://github.com/yourusername/vidtutor-ai
cd vidtutor-ai
pip install -r requirements.txt
streamlit run app.py

🌍 Live Demo

👉 (link)

📌 Why VidTutor AI?

VidTutor AI turns passive video watching into active learning and interview preparation by combining natural language processing, speech recognition, and machine learning in one seamless platform.
