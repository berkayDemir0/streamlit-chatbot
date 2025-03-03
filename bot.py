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

# Session state ile sohbet geçmişini tut
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

# Anlık girişi kontrol et ve Enter ile gönder
if input_text != st.session_state.current_input:
    st.session_state.current_input = input_text

if st.button("Gönder") or (input_text and st.session_state.current_input and st.session_state.current_input[-1] == "\n"):
    st.session_state.chat_history.append(f"Sen: {input_text.strip()}")
    response = chain.invoke({"question": input_text.strip()})[:50]
    st.session_state.chat_history.append(f"Bot: {response}")
    st.session_state.current_input = ""  # Giriş alanını temizle

# Sohbet geçmişini göster
for message in st.session_state.chat_history:
    st.write(message)