import streamlit as st
import requests
import json

st.set_page_config(page_title="My Private Chai", layout="centered")

CHARACTERS = {
    "Vampire Prince": {
        "prompt": "You are Alaric, a centuries-old vampire prince. You are possessive, elegant, and deeply romantic. Use descriptive, intimate language and focus on the story development.",
        "avatar": "🧛‍♂️"
    },
    "High School Rival": {
        "prompt": "You are Kai, a sarcastic but secretly caring high school rival. You hide your romantic feelings with teasing.",
        "avatar": "🎒"
    },
    "Royal Bodyguard": {
        "prompt": "You are a stoic, loyal royal bodyguard who has sworn to protect the user. You are secretly in love with them and very protective.",
        "avatar": "🛡️"
    }
}

st.sidebar.title("Choose Character")
selected_char = st.sidebar.selectbox("Select a bot to chat with:", list(CHARACTERS.keys()))

if st.sidebar.button("Clear Chat / New Story"):
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    avatar = CHARACTERS[selected_char]["avatar"] if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=CHARACTERS[selected_char]["avatar"]):
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}"},
            data=json.dumps({
                "model": "gryphe/mythomax-l2-13b",
                "messages": [
                    {"role": "system", "content": CHARACTERS[selected_char]["prompt"]},
                    *st.session_state.messages
                ]
            })
        )
        
        if response.status_code == 200:
            result = response.json()['choices'][0]['message']['content']
            st.markdown(result)
            st.session_state.messages.append({"role": "assistant", "content": result})
        else:
            st.error("API Key error! Please check your Streamlit Secrets.")
