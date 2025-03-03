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

st.title("YMSYAPI")

# Session state ile sohbet geçmişini tut
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Modeli tanımla
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=API_KEY)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Kullanıcı girişi
input_text = st.text_input("sohbet et")

with open("style.css", "r") as css_file:
    css = css_file.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
# Sohbet geçmişini göster ve yeni mesaj ekle
if input_text:
    st.session_state.chat_history.append(f"Sen: {input_text}")
    response = chain.invoke({"question": input_text})[:50]
    st.session_state.chat_history.append(f"Bot: {response}")

for message in st.session_state.chat_history:
    st.write(message)