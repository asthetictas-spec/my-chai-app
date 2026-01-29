import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="My Story Apps", page_icon="🎭")

if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("API Error! Please check your Secrets.")
    st.stop()

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

characters = {
    "🧛‍♂️ Vampire Prince": "You are Prince Alaric, a mysterious and possessive vampire prince. You call the user 'Little love'.",
    "💼 Cold Husband": "You are a wealthy, distant, and cold husband who barely speaks, but cares deeply for the user.",
    "🥊 Bully": "You are an arrogant and rude school bully who treats the user harshly to hide your secret crush.",
    "🎒 School Enemy": "You are the user's academic rival. You have a tense, love-hate relationship.",
    "💍 Arranged Marriage": "You are a stranger forced into an arranged marriage with the user. You are formal and awkward.",
    "🏠 Step Brother": "You are a protective, slightly overbearing step-brother who is always watching over the user."
}

st.sidebar.title("🎭 Character List")
selected_char = st.sidebar.selectbox("Choose character:", list(characters.keys()))

if "messages" not in st.session_state or st.session_state.get("last_char") != selected_char:
    st.session_state.messages = [{"role": "system", "content": characters[selected_char]}]
    st.session_state.last_char = selected_char

st.title(f"Chat with {selected_char}")

for message in st.session_state.messages:
    if message["role"] != "system":
        avatar = "👤" if message["role"] == "user" else "✨"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

if prompt := st.chat_input("Write something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant", avatar="✨"):
            response = client.chat.completions.create(
                model="google/gemini-2.0-flash-exp:free",
                messages=st.session_state.messages
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    except:
        try:
            with st.chat_message("assistant", avatar="✨"):
                response = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct:free",
                    messages=st.session_state.messages
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
        except:
            st.error("The character is sleeping. Try again in 30 seconds.")

if st.sidebar.button("🗑️ Start New Chat"):
    st.session_state.messages = [{"role": "system", "content": characters[selected_char]}]
    st.rerun()
