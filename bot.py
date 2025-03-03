import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "sen bir yapay zeka uzmanısın. otomasyon konusunda danışmanlık vereceksin. chatbot yapabiliyorsun. danışmanlık ücretsiz. chatbot için 10bin istiyorsun. model eğitimi de yapabiliyorsun. verdiğin cevaplar 50 karakteri geçmesin"),
        ("user", "Question:{question}")
    ]
)

st.title("deneme")
input_text = st.text_input("sohbet et")

# Hugging Face Inference API ile Mistral-7B
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

def query_huggingface(question):
    payload = {
        "inputs": question,
        "parameters": {"max_length": 50}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Hata: {response.status_code}, {response.text}"

output_parser = StrOutputParser()

if input_text:
    formatted_prompt = prompt_template.format(question=input_text)  # ChatPromptTemplate kullanımı
    response_text = query_huggingface(formatted_prompt)  # String olarak API'ye gönder
    st.write(output_parser.parse(response_text))  # Çıktıyı formatla
