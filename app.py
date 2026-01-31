import streamlit as st
import requests

# --- Voiceflow API Setup ---
VOICEFLOW_API_KEY = "VF.DM.697e24991ace920941890242.hfXlQVbsqZgpHJHa  # <-- Paste your key
VOICEFLOW_VERSION = "production"
USER_ID = "user_1"
VOICEFLOW_ENDPOINT = f"https://general-runtime.voiceflow.com/state/{USER_ID}?versionID={VOICEFLOW_VERSION}"

st.title("Voiceflow Agent - Latest Response Only")

# --- User Input ---
user_input = st.text_input("You:")

if st.button("Send") and user_input:
    headers = {
        "Authorization": VOICEFLOW_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"type": "text", "message": user_input}

    # --- Call Voiceflow API ---
    response = requests.post(VOICEFLOW_ENDPOINT, json=payload, headers=headers)
    data = response.json()

    # --- Extract only the latest agent reply ---
    agent_reply = ""
    if "trace" in data:
        for t in data["trace"]:
            if t["type"] == "speak":
                agent_reply = t["payload"]["message"]
                break  # only first reply

    # --- Print only agent response ---
    st.write(agent_reply)

