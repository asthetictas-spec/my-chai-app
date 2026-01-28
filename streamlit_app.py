import streamlit as st
import requests
import json
import os

# ১. পেজ সেটিংস এবং ডিজাইন
st.set_page_config(page_title="My Private Chai", layout="centered")

# ২. চ্যাট হিস্ট্রি ফাইল সেটআপ (Old Chat সেভ করার জন্য)
CHAT_FILE = "chat_history_save.json"

def load_history():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(messages):
    with open(CHAT_FILE, "w") as f:
        json.dump(messages, f)

# ৩. ক্যারেক্টার এবং তাদের ছবির লিঙ্ক
CHARACTERS = {
    "Vampire Prince": {
        "prompt": "You are Alaric, a centuries-old vampire prince. You are possessive, elegant, and deeply romantic.",
        "avatar": "https://i.pinimg.com/736x/a9/3a/0e/a93a0e10787e67f730c4e09f53835c24.jpg"
    }
}

# ৪. সেশন স্টেট এবং হিস্ট্রি লোড
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

# ৫. সাইডবার সেটিংস
st.sidebar.title("Chai Settings")
if st.sidebar.button("Clear Chat / New Story"):
    st.session_state.messages = []
    if os.path.exists(CHAT_FILE):
        os.remove(CHAT_FILE)
    st.rerun()

# ৬. আগের চ্যাট স্ক্রিনে দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])

# ৭. নতুন মেসেজ ইনপুট এবং এআই রেসপন্স
if prompt := st.chat_input("Type your message..."):
    # আপনার ছবি
    user_pic = "https://i.pinimg.com/736x/5c/8a/7e/5c8a7e937d7a4f938f38f38f38f38f38.jpg"
    
    # ইউজারের মেসেজ সেভ এবং শো করা
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": user_pic})
    with st.chat_message("user", avatar=user_pic):
        st.markdown(prompt)

    # অ্যালারিকের উত্তর আনা
    with st.chat_message("assistant", avatar=CHARACTERS["Vampire Prince"]["avatar"]):
        try:
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
            
            # মেমোরিতে সেভ করা
            st.session_state.messages.append({"role": "assistant", "content": bot_msg, "avatar": CHARACTERS["Vampire Prince"]["avatar"]})
            save_history(st.session_state.messages)
        except:
            st.error("API Error! Please check your Secrets in Streamlit.")
