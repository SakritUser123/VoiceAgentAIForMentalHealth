import streamlit as st
import requests

# --- Voiceflow API Setup ---
VOICEFLOW_API_KEY = "VF.DM.697e24991ace920941890242.hfXlQVbsqZgpHJHa"  # <-- Paste your key here
VOICEFLOW_VERSION = "production"  # usually 'production'
USER_ID = "user_1"  # unique session ID for this user
VOICEFLOW_ENDPOINT = f"https://general-runtime.voiceflow.com/state/{USER_ID}?versionID={VOICEFLOW_VERSION}"

# --- Initialize session ---
if "conversation" not in st.session_state:
    st.session_state.conversation = []

st.title("Voiceflow Agent Test")

# --- User Input ---
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

    # --- Call Voiceflow API ---
    response = requests.post(VOICEFLOW_ENDPOINT, json=payload, headers=headers)
    data = response.json()

    # --- Extract and Print Agent Response ---
    agent_reply = ""
    if "trace" in data:
        for t in data["trace"]:
            if t["type"] == "speak":
                agent_reply = t["payload"]["message"]
                st.session_state.conversation.append(("Agent", agent_reply))

    st.session_state.conversation.append(("User", user_input))

# --- Display Conversation ---
for speaker, message in st.session_state.conversation:
    st.write(f"**{speaker}:** {message}")
