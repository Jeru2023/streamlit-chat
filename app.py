import openai
import toml
import streamlit as st
from streamlit_option_menu import option_menu
import os

st.set_page_config(page_title='ChatGPT Assistant', layout='wide', page_icon='🍋')

with open(".streamlit/secrets.toml", "r") as f:
	config = toml.load(f)

openai.api_key = config["OPENAI_KEY"]
os.environ["http_proxy"]="http://127.0.0.1:7890"
os.environ["https_proxy"]="http://127.0.0.1:7890"

BASE_PROMPT = [{"role": "system", "content": "You are a helpful assistant."}]

topbar = option_menu(None, ["Home", "Upload",  "Tasks", 'Settings'], 
	icons=['house', 'cloud-upload', "list-task", 'gear'], 
	menu_icon="cast", default_index=0, orientation="horizontal",
	styles={
		"nav-link": {"--hover-color": "#eee"},		
	}
)	

with st.sidebar:
	# st.header("Control Panel")
	st.markdown("# Control Panel 📌")
	context_level = st.slider('Context Level 👇', 1, 10, 4, 1)
	temperature = st.slider('Temperature 👇', 0.0, 2.0, 1.0, 0.5)
	top_p = st.slider('Top P 👇', 0.1, 1.0, 1.0, 0.1)
	presence_penalty = st.slider('Presence Penalty 👇', -2.0, 2.0, 0.0, 0.1)
	frequency_penalty = st.slider('Frequence Penalty 👇', -2.0, 2.0, 0.0, 0.1)
	#https://platform.openai.com/docs/api-reference/completions/create

	
	uploaded_files = st.file_uploader("Choose a PDF file", accept_multiple_files=True)
	for uploaded_file in uploaded_files:
		bytes_data = uploaded_file.read()
		st.write("filename:", uploaded_file.name)
		st.write(bytes_data)
		
if 'past' not in st.session_state:
	st.session_state['past'] = []

if "generated" not in st.session_state:
    st.session_state["generated"] = BASE_PROMPT
	
st.session_state["key"] = 0

def parse_data(data):
	role = data['role']
	content = data['content']
	output = f"{role}: {content}"
	return output

def show_messages(text):
	content = []
	for i in range(1, len(st.session_state['generated']), 1):
		past_message = parse_data(st.session_state["past"][i-1])
		generated_message = parse_data(st.session_state["generated"][i])
		content.append(past_message)
		content.append(generated_message)
	print('use widget gen:',st.session_state["generated"])
	print('use widget past:',st.session_state["past"])
	st.session_state["key"] += 1
	text.text_area("Messages", value=str("\n".join(content)), key=st.session_state["key"], height=600)

	
st.header("Welcome to Jeru's CHATBOT 🍋")

text = st.empty()
show_messages(text)

prompt = st.text_input("Prompt", placeholder="Enter your message here...")

if st.button("Send"):
	with st.spinner("Generating response..."):
	
		st.session_state["past"].append({"role": "user", "content": prompt})
		#TODO：to add context
		response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
		message_response = response["choices"][0]["message"]["content"]
		st.session_state["generated"].append({"role": "system", "content": message_response})
	
		show_messages(text)