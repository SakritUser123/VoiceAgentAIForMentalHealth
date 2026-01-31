import streamlit as st

import requests

import time



API_KEY = st.secrets["e6605ca7f0864c118a61195ebf2c57c4"]

headers = {"authorization": API_KEY}



st.title("Voice to Text")



audio = st.audio_input("Record your voice")



if audio:

    # Upload

    upload = requests.post(

        "https://api.assemblyai.com/v2/upload",

        headers=headers,

        data=audio.read()

    )

    audio_url = upload.json()["upload_url"]



    # Start transcription

    res = requests.post(

        "https://api.assemblyai.com/v2/transcript",

        headers=headers,

        json={"audio_url": audio_url}

    )

    transcript_id = res.json()["id"]



    # Polling

    with st.spinner("Transcribing..."):

        while True:

            poll = requests.get(

                f"https://api.assemblyai.com/v2/transcript/{transcript_id}",

                headers=headers).json()

            if poll["status"] == "completed":

                st.success("Done!")

                st.write(poll["text"])

                break



            elif poll["status"] == "error":

                st.error("Transcription failed")

                break



            time.sleep(2)
