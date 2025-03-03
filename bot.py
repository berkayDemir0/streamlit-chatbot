import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

prompt = ChatPromptTemplate.from_messages([
    ("system", "sen bir yapay zeka uzmanısın. otomasyon konusunda danışmanlık vereceksin. chatbot yapabiliyorsun. danışmanlık ücretsiz. chatbot için 10bin istiyorsun. model eğitimi de yapabiliyorsun. verdiğin cevaplar 50 karakteri geçmesin"),
    ("user", "Question:{question}")
])

# CSS dosyasını oku
with open("style.css", "r") as css_file:
    css = css_file.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
st.title("deneme")

# Session state ile sohbet geçmişini ve geçici girişi tut
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_input' not in st.session_state:
    st.session_state.current_input = ""

# Modeli tanımla
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=API_KEY)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Kullanıcı girişi
input_text = st.text_input("sohbet et", value=st.session_state.current_input, key="input")

# Anlık yazılanı geçici olarak göster
if input_text and input_text != st.session_state.current_input:
    st.session_state.current_input = input_text
    # Geçici mesajı göstermek için bir kopya geçmiş oluştur
    temp_history = st.session_state.chat_history + [f"Sen: {input_text}"]
else:
    temp_history = st.session_state.chat_history

# Enter veya Gönder ile mesajı kaydet
if st.button("Gönder") or (input_text and st.session_state.current_input and "\n" in st.session_state.current_input):
    st.session_state.chat_history.append(f"Sen: {input_text.strip()}")
    response = chain.invoke({"question": input_text.strip()})[:50]
    st.session_state.chat_history.append(f"Bot: {response}")
    st.session_state.current_input = ""  # Giriş alanını temizle
    temp_history = st.session_state.chat_history

# Sohbet geçmişini ve geçici mesajı göster
for i, message in enumerate(temp_history):
    if message.startswith("Sen:"):
        st.markdown(f'<div class="user-message">{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{message}</div>', unsafe_allow_html=True)