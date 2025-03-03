import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Ortam değişkenlerini yükle
load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

# Prompt şablonu
prompt = ChatPromptTemplate.from_messages([
    ("system", "Sen bir yapay zeka uzmanısın. Cevapların 50 karakteri geçmesin."),
    ("user", "Soru: {question}")
])

# CSS dosyasını yükle
with open("style.css", "r") as css_file:
    css = css_file.read()

# CSS ve header gizleme
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Giriş mesajı
st.markdown('<div class="intro-text">Merhaba, ben yapay zeka asistanınız. Size nasıl yardımcı olabilirim?</div>', unsafe_allow_html=True)

# Sohbet geçmişini sakla
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Modeli tanımla (eski model: gemini-1.5-pro)
llm = ChatGoogleGenerativeAI(model="gemini-2.0", google_api_key=API_KEY)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Sohbet geçmişini göster
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="bot-bubble"><img src="bot_logo.png" class="bot-logo">{message["content"]}</div>',
            unsafe_allow_html=True
        )

# Mesaj giriş formu (Enter veya butonla gönderim)
with st.form(key="chat_form", clear_on_submit=True):
    input_text = st.text_input("Mesaj yaz", placeholder="Sorunuzu buraya yazın...")
    submit_button = st.form_submit_button("Gönder")

    # Enter veya butonla mesaj gönder
    if (submit_button or input_text) and input_text.strip():
        st.session_state.chat_history.append({"role": "user", "content": input_text})
        response = chain.invoke({"question": input_text})[:50]
        st.session_state.chat_history.append({"role": "bot", "content": response})
        st.rerun()  # Ekranı güncelle