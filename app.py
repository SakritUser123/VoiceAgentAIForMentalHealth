import streamlit as st
import requests

# --- Voiceflow API Setup ---
VOICEFLOW_API_KEY = "VF.DM.697e24991ace920941890242.hfXlQVbsqZgpHJHa"
VOICEFLOW_VERSION = "production"
USER_ID = "user_1"
VOICEFLOW_ENDPOINT = f"https://general-runtime.voiceflow.com/state/{USER_ID}?versionID={VOICEFLOW_VERSION}"

st.title("Voiceflow Agent - Latest Response Only")

# --- User Input ---
user_input = st.text_input("Type your message:")

if st.button("Send") and user_input:
    headers = {
        "Authorization": VOICEFLOW_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "type": "text",
        "message": user_input
    }

    try:
        response = requests.post(VOICEFLOW_ENDPOINT, json=payload, headers=headers)
        data = response.json()

        # --- Extract only agent reply ---
        agent_reply = None
        if "trace" in data and isinstance(data["trace"], list):
            for t in data["trace"]:
                # Look for a 'speak' type (Voiceflow text response)
                if t.get("type") == "speak":
                    agent_reply = t["payload"].get("message")
                    break

        if agent_reply:
            st.write(agent_reply)
        else:
            st.write(" No response from the agent. Try again.")

    except Exception as e:
        st.write(f"Error connecting to Voiceflow API: {e}")


