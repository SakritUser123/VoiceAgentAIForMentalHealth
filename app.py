import streamlit as st
import openai
import requests
import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play


ASSEMBLYAI_API_KEY = "e6605ca7f0864c118a61195ebf2c57c4"
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

st.title("Voice AI Assistant ")


audio_file = st.file_uploader("Upload your voice (wav/mp3)", type=["wav","mp3"])

if audio_file:
    # Save the uploaded file
    audio_bytes = audio_file.read()
    
    
    st.info("Transcribing audio...")
    headers = {"authorization": ASSEMBLYAI_API_KEY}
    response = requests.post(
        "https://api.assemblyai.com/v2/upload",
        headers=headers,
        files={"file": audio_bytes}
    )
    audio_url = response.json()['upload_url']

   
    transcript_response = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers=headers,
        json={"audio_url": audio_url}
    )
    transcript_id = transcript_response.json()['id']

  
    st.info("Processing transcription...")
    import time
    while True:
        r = requests.get(f"https://api.assemblyai.com/v2/transcript/{transcript_id}", headers=headers)
        result = r.json()
        if result['status'] == 'completed':
            text = result['text']
            break
        elif result['status'] == 'failed':
            st.error("Transcription failed")
            text = ""
            break
        time.sleep(2)

    st.success("Transcription complete!")
    st.write("You said:", text)


    st.info("Generating AI response...")
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}]
    )
    answer = completion.choices[0].message.content
    st.write("AI response:", answer)

    tts = gTTS(answer)
    tts_fp = BytesIO()
    tts.write_to_fp(tts_fp)
    tts_fp.seek(0)

    # Convert BytesIO to playable AudioSegment
    audio = AudioSegment.from_file(tts_fp, format="mp3")
    st.audio(audio.export(format="mp3").read(), format="audio/mp3")


