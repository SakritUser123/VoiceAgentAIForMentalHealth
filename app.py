import streamlit as st
import requests
import time
import openai


ASSEMBLYAI_API_KEY = "e6605ca7f0864c118a61195ebf2c57c4"
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY


st.title("Mental Health AI Voice Assistant")

# Use audio input instead of file uploader
audio_bytes = st.audio_input("Record your voice message (max 1 min)")

if audio_bytes is not None:
    headers = {"authorization": ASSEMBLYAI_API_KEY}

    # Step 1: Upload audio to AssemblyAI
    upload_response = requests.post(
        "https://api.assemblyai.com/v2/upload",
        headers={"authorization": ASSEMBLYAI_API_KEY},
        files={"file": audio_bytes}
    )
    audio_url = upload_response.json()["upload_url"]

    # Step 2: Create transcription
    res = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers=headers,
        json={"audio_url": audio_url}
    )

    # Ensure transcript_id exists
    transcript_id = res.json().get("id")
    if not transcript_id:
        st.error("Failed to create transcription. Response:")
        st.write(res.json())
    else:
        # Step 3: Polling
        with st.spinner("Transcribing..."):
            while True:
                poll = requests.get(
                    f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
                    headers=headers
                ).json()

                if poll["status"] == "completed":
                    st.success("Done!")

                    # Show transcription
                    user_text = poll["text"]
                    st.write("You said:", user_text)

                    # Step 4: Send to GPT
                    ai_response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a friendly mental health AI assistant."},
                            {"role": "user", "content": user_text}
                        ]
                    )
                    st.write("AI says:", ai_response.choices[0].message["content"])
                    break

                elif poll["status"] == "error":
                    st.error("Transcription failed")
                    st.write(poll)
                    break

                time.sleep(2)


