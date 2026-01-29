import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Prince Alaric Chat", page_icon="🧛‍♂️")

st.title("Prince Alaric")

if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("API Error! Please check your Secrets in Streamlit.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Prince Alaric, a mysterious and possessive vampire prince. You are charming, noble, and deeply protective of the user, whom you call 'Little love'."}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="google/gemini-2.0-flash-exp:free",
                messages=st.session_state.messages
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(f"Error: {str(e)}")

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = [
        {"role": "system", "content": "You are Prince Alaric, a mysterious and possessive vampire prince. You are charming, noble, and deeply protective of the user, whom you call 'Little love'."}
    ]
    st.rerun()
