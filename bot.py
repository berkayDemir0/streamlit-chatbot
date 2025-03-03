import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')

# Chat prompt şablonu
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system",
         "Sen bir yapay zeka uzmanısın. Otomasyon konusunda danışmanlık vereceksin. Chatbot yapabiliyorsun. Danışmanlık ücretsiz. Chatbot için 10 bin istiyorsun. Model eğitimi de yapabiliyorsun. Verdiğin cevaplar 50 karakteri geçmesin."),
        ("user", "{question}")
    ]
)

st.title("deneme")
input_text = st.text_input("Sohbet et")

# Hugging Face API bağlantı bilgileri
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}


def query_huggingface(user_input):
    """ Hugging Face API'ye kullanıcı girdisini gönder ve yanıtı al """
    payload = {
        "inputs": user_input,  # Sadece kullanıcının sorusunu API'ye gönderiyoruz
        "parameters": {"max_length": 50}
    }
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Hata: {response.status_code}, {response.text}"


output_parser = StrOutputParser()

if input_text:
    formatted_prompt = prompt_template.format(question=input_text)  # Promptu oluştur
    user_query = input_text  # Sadece kullanıcı girdisini API'ye gönderiyoruz

    response_text = query_huggingface(user_query)  # Hugging Face API'ye gönder
    st.write(output_parser.parse(response_text))  # Çıktıyı yazdır
# Çıktıyı formatla
