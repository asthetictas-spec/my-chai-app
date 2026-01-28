import streamlit as st
import requests
import json
import os

# পেজ টাইটেল এবং স্টাইল
st.set_page_config(page_title="My Private Chai", layout="centered")

# চ্যাট হিস্ট্রি ফাইল সেভ করার নিয়ম
CHAT_FILE = "chat_history_save.json"

def load_history():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(messages):
    with open(CHAT_FILE, "w") as f:
        json.dump(messages, f)

# ক্যারেক্টার লিস্ট
CHARACTERS = {
    "Vampire Prince": {
        "prompt": "You are Alaric, a centuries-old vampire prince. You are possessive, elegant, and deeply romantic.",
        "avatar": "🧛‍♂️"
    }
}

# সেশন স্টেট এবং হিস্ট্রি লোড
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

# চ্যাট ইন্টারফেস দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])

# ইউজার মেসেজ ইনপুট
if prompt := st.chat_input("Type your message..."):
    user_avatar = "👸"
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": user_avatar})
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt)

    # এআই থেকে উত্তর আনা
    with st.chat_message("assistant", avatar=CHARACTERS["Vampire Prince"]["avatar"]):
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}"},
            data=json.dumps({
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [{"role": "system", "content": CHARACTERS["Vampire Prince"]["prompt"]}] + 
                            [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            })
        )
        bot_msg = response.json()['choices'][0]['message']['content']
        st.markdown(bot_msg)
        
        # সেভ করা
        st.session_state.messages.append({"role": "assistant", "content": bot_msg, "avatar": CHARACTERS["Vampire Prince"]["avatar"]})
        save_history(st.session_state.messages)

# নতুন চ্যাট শুরু করার বাটন
if st.sidebar.button("Clear Chat / New Story"):
    st.session_state.messages = []
    if os.path.exists(CHAT_FILE):
        os.remove(CHAT_FILE)
    st.rerun()
