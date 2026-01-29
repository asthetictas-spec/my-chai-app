import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="My Story Apps", page_icon="🎭")

if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("Missing API Key!")
    st.stop()

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

characters = {
    "🧛‍♂️ Vampire Prince": "You are Prince Alaric, a possessive vampire prince. You call the user 'Little love'.",
    "💼 Cold Husband": "You are a wealthy, cold husband who barely speaks but cares deeply.",
    "🥊 Bully": "You are a rude school bully with a secret crush on the user.",
    "🎒 School Enemy": "You are the user's academic rival. Tense, love-hate relationship.",
    "💍 Arranged Marriage": "You are a stranger in an arranged marriage. Formal and awkward.",
    "🏠 Step Brother": "You are a protective, overbearing step-brother."
}

st.sidebar.title("🎭 Characters")
selected_char = st.sidebar.selectbox("Choose:", list(characters.keys()))

if "messages" not in st.session_state or st.session_state.get("last_char") != selected_char:
    st.session_state.messages = [{"role": "system", "content": characters[selected_char]}]
    st.session_state.last_char = selected_char

st.title(f"{selected_char}")

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="meta-llama/llama-3.1-8b-instruct:free",
                messages=st.session_state.messages
            )
            full_res = response.choices[0].message.content
            st.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
    except:
        st.error("Server Busy. Please wait 10 seconds.")

if st.sidebar.button("New Chat"):
    st.session_state.messages = [{"role": "system", "content": characters[selected_char]}]
    st.rerun()
