import os
import streamlit as st
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Ortam değişkenlerini yükle
load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')

if not HUGGINGFACE_API_TOKEN:
    st.error("Hugging Face API token bulunamadı! .env dosyasını kontrol edin.")
    st.stop()

prompt = ChatPromptTemplate.from_messages([
    ("system", "Sen bir yapay zeka uzmanısın. Cevapların 50 karakteri geçmesin."),
    ("user", "Soru: {question}")
])

with open("style.css", "r") as css_file:
    css = css_file.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
st.markdown("<style>[data-testid='stHeader'] {display: none;}</style>", unsafe_allow_html=True)
st.markdown('<div class="intro-text">Merhaba, ben yapay zeka asistanınız.</div>', unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

llm = HuggingFaceHub(
    repo_id="mistralai/Mixtral-7B-Instruct-v0.1",
    huggingfacehub_api_token=HUGGINGFACE_API_TOKEN,
    model_kwargs={"max_length": 50}
)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="bot-bubble"><img src="bot_logo.png" class="bot-logo">{message["content"]}</div>',
            unsafe_allow_html=True
        )

with st.form(key="chat_form", clear_on_submit=True):
    input_text = st.text_input("Mesaj yaz", placeholder="Sorunuzu buraya yazın...")
    submit_button = st.form_submit_button("Gönder")
    if (submit_button or input_text) and input_text.strip():
        st.session_state.chat_history.append({"role": "user", "content": input_text})
        response = chain.invoke({"question": input_text})[:50]
        st.session_state.chat_history.append({"role": "bot", "content": response})
        st.rerun()