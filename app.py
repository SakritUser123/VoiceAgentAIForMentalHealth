import requests
import os
import streamlit as st

api_key = os.getenv('VF_API_KEY', 'VF.DM.697e24991ace920941890242.hfXlQVbsqZgpHJHa')

def interact(user_id, request):
    url = f'https://general-runtime.voiceflow.com/state/user/{user_id}/interact'
    payload = { 'request': request }
    headers = { 
        'Authorization': api_key,
    }
    params = {
        'versionID': 'production'
    }
    
    response = requests.post(url, json=payload, headers=headers, params=params)
    return response.json()

st.set_page_config(page_title="Mental Health Assistant", layout="wide")

tab1, tab2 , tab3 = st.tabs(["Search it Up!", "Chatbot", "Voice agent"])

with tab1:
    st.title("Search up the problem!")
    st.write("Do you feel like you can't trust the voice chat bot? No worries! You can also search up your problems online.")
    options = ["Academic Stress", "Stress from a Big Event", "You need something funny?", "Motivation Speeches", "Relatable Stress", "What is anxiety?"]
    query = st.selectbox("Enter search term", options)
    search_url = f"https://www.google.com/search?q={query}"
    st.markdown(f'<a href="{search_url}" target="_blank">Click to search: {query}</a>', unsafe_allow_html=True)

with tab2:
    st.title("Chatbot Assistant")
    st.write("Do you feel like you need to talk to someone, but you feel like you can talk to no one? Although this AI doesn't actually have feelings so it can't empathize, it can potentially help you by providing guidance, providing you with exercises that reduce stress and improve mental health, gives advice on topics you feel down about, basically being your AI mental assistant.")
    
    # Initialize session state for conversation
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'user_id' not in st.session_state:
        st.session_state.user_id = 'user123'
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("How do you feel...")
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get bot response
        result = interact(st.session_state.user_id, {'type': 'text', 'payload': user_input})
        
        # Extract and display bot message
        bot_message = None
        for item in result:
            if item.get('type') == 'text' and 'message' in item.get('payload', {}):
                bot_message = item['payload']['message']
                break
        
        if bot_message:
            st.session_state.messages.append({"role": "assistant", "content": bot_message})
            with st.chat_message("assistant"):
                st.write(bot_message)
