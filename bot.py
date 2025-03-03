import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain import requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","sen bir yapay zeka uzmanısın. otomasyon konusunda danışmanlık vereceksin. chatbot yapabiliyorsun. danışmanlık ücretsiz. chatbot için 10bin istiyorsun. model eğitimi de yapabiliyorsun. verdiğin cevaplar 50 karakteri geçmesin"),
        ("user","Question:{question}")
    ]
)

st.title("YMSYAPI")
input_text=st.text_input("sohbet et")
# Modeli "gemini-pro" yerine "gemini-pro" olarak değiştirdik
llm = ChatGoogleGenerativeAI(model="gemini-2.0", google_api_key=API_KEY)


output_parsers=StrOutputParser()
chain=prompt|llm|output_parsers

if input_text:
  st.write(chain.invoke({"question":input_text}))




