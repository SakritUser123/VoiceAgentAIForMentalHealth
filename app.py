

import streamlit as st
import requests


VOICEFLOW_API_KEY = "VF.DM.697e24991ace920941890242.hfXlQVbsqZgpHJHa"
VOICEFLOW_VERSION = "production"  
VOICEFLOW_ENDPOINT = f"https://general-runtime.voiceflow.com/state/user_id?versionID={VOICEFLOW_VERSION}"


if "conversation" not in st.session_state:
    st.session_state.conversation = []


st.title("Voiceflow + Streamlit Agent")

user_input = st.text_input("You:", key="input_text")

if st.button("Send") and user_input:
    headers = {
        "Authorization": VOICEFLOW_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "type": "text",
        "message": user_input
    }

    # Call Voiceflow API
    response = requests.post(VOICEFLOW_ENDPOINT, json=payload, headers=headers)
    data = response.json()

    # Voiceflow usually returns output text in data["trace"]
    if "trace" in data:
        for t in data["trace"]:
            if t["type"] == "speak":
                agent_reply = t["payload"]["message"]
                st.session_state.conversation.append(("Agent", agent_reply))

    st.session_state.conversation.append(("User", user_input))

for speaker, message in st.session_state.conversation:
    st.write(f"**{speaker}:** {message}")
