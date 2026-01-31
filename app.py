import streamlit as st
import requests
import openai
from io import BytesIO
import time


OPENAI_API_KEY = "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"
ASSEMBLYAI_API_KEY = "e6605ca7f0864c118a61195ebf2c57c4"

openai.api_key = OPENAI_API_KEY

st.title("Voice AI Assistant ")


audio_file = st.file_uploader("Upload your voice (wav/mp3)", type=["wav", "mp3"])

if audio_file:
    st.info("Uploading audio to AssemblyAI...")

    # Upload audio to AssemblyAI
    headers = {"authorization": ASSEMBLYAI_API_KEY}
    response = requests.post(
        "https://api.assemblyai.com/v2/upload",
        headers=headers,
        files={"file": audio_file.read()}
    )
    audio_url = response.json()["upload_url"]


    st.info("Transcribing...")
    transcript_response = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers=headers,
        json={"audio_url": audio_url}
    )
    transcript_id = transcript_response.json()["id"]


    while True:
        r = requests.get(f"https://api.assemblyai.com/v2/transcript/{transcript_id}", headers=headers)
        result = r.json()
        if result["status"] == "completed":
            user_text = result["text"]
            break
        elif result["status"] == "failed":
            st.error("Transcription failed")
            user_text = ""
            break
        time.sleep(2)

    st.success("Transcription complete!")
    st.write("You said:", user_text)


    st.info("Generating AI response...")
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_text}]
    )
    ai_text = completion.choices[0].message.content
    st.write("AI response:", ai_text)


    st.info("Converting AI response to speech...")
    tts_response = openai.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=ai_text
    )

    audio_bytes = BytesIO(tts_response.read())
    st.audio(audio_bytes, format="audio/mpeg")

