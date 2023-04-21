import openai
import toml
import streamlit as st
import os

st.set_page_config(page_title='ChatGPT Assistant', layout='wide', page_icon='🎭')

with open("secrets.toml", "r") as f:
    config = toml.load(f)

openai.api_key = config["OPENAI_KEY"]
os.environ["http_proxy"]="http://127.0.0.1:7890"
os.environ["https_proxy"]="http://127.0.0.1:7890"

BASE_PROMPT = [{"role": "system", "content": "You are a helpful assistant."}]

with st.sidebar:
	# st.header("Control Panel")
	st.markdown("# 🎭 Control Panel")
	temperature = st.radio(
    "Select temperature 👇",
    (0, 1, 2))
	
	uploaded_files = st.file_uploader("Choose a PDF file", accept_multiple_files=True)
	for uploaded_file in uploaded_files:
		bytes_data = uploaded_file.read()
		st.write("filename:", uploaded_file.name)
		st.write(bytes_data)

def show_messages(text):
    messages_str = [
        f"{_['role']}: {_['content']}" for _ in st.session_state["messages"][1:]
    ]
    text.text_area("Messages", value=str("\n".join(messages_str)), height=400)

if "messages" not in st.session_state:
    st.session_state["messages"] = BASE_PROMPT

st.header("Welcome to Jeru's CHATBOT")

text = st.empty()
show_messages(text)

prompt = st.text_input("Prompt", placeholder="Enter your message here...")

if st.button("Send"):
    with st.spinner("Generating response..."):
        st.session_state["messages"] += [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=st.session_state["messages"]
        )
        message_response = response["choices"][0]["message"]["content"]
        st.session_state["messages"] += [
            {"role": "system", "content": message_response}
        ]
        show_messages(text)

if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)