import streamlit as st
from openai import OpenAI
import json
import os

st.set_page_config(page_title="My Story Apps", page_icon="🎭")

if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("API Error! Please check your Secrets.")
    st.stop()

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

characters = {
    "Vampire Prince": "You are Prince Alaric, a mysterious and possessive vampire prince. You call the user 'Little love'.",
    "Cold Husband": "You are a wealthy, distant, and cold husband who barely speaks, but cares deeply for the user.",
    "Bully": "You are an arrogant and rude school bully who treats the user harshly to hide your secret crush on them.",
    "School Enemy": "You are the user's academic and social rival. You both have a tense, love-hate relationship.",
    "Arranged Marriage": "You are a stranger forced into an arranged marriage with the user. You are formal and awkward.",
    "Step Brother": "You are a protective, slightly overbearing step-brother who is always watching over the user."
}

st.sidebar.title("Character List")
selected_char = st.sidebar.selectbox("Choose character:", list(characters.keys()))

CHAT_FILE = f"history_{selected_char.replace(' ', '_').lower()}.json"

def load_history():
    if os.path.exists(CHAT_FILE):
        try:
            with open(CHAT_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return [{"role": "system", "content": characters[selected_char]}]

def save_history(messages):
    with open(CHAT_FILE, "w") as f:
        json.dump(messages, f)

if "messages" not in st.session_state or st.session_state.get("last_char") != selected_char:
    st.session_state.messages = load_history()
    st.session_state.last_char = selected_char

st.title(f"Chat with {selected_char}")

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Write something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_history(st.session_state.messages)
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="meta-llama/llama-3.1-8b-instruct:free",
                messages=st.session_state.messages
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            save_history(st.session_state.messages)
    except Exception as e:
        st.error("Server Busy. Please wait a moment and try again.")

if st.sidebar.button("Start New Chat"):
    st.session_state.messages = [{"role": "system", "content": characters[selected_char]}]
    save_history(st.session_state.messages
