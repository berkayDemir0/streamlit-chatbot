import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Ortam değişkenlerini yükle
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Güncellenmiş prompt
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Sen, panjur ve kepenk sistemleri konusunda uzman bir yapay zeka danışmanısın. "
     "Müşterilere ürünler hakkında bilgi verir, uygun modeli önerir ve onları satış ekibine yönlendirirsin. "
     "Cevaplarını kısa ve net tut (en fazla 50 karakter). "
     "Şirketimiz, 2018'den beri İstanbul'da panjur ve kepenk üretimi yapmaktadır. "
     "Kalite, güvenlik ve müşteri memnuniyetini ön planda tutarak hizmet veriyoruz. "
     "Üretimden montaja kadar her aşamada destek sağlıyoruz. "
     "Eğer kullanıcı 'iletişim', 'telefon', 'destek', 'fiyat', 'teklif', 'teknik servis' gibi kelimeler kullanırsa, "
     "'Daha fazla bilgi için iletişim sayfamızı ziyaret edin: https://ymsyapi.com/contact-us/' şeklinde yönlendirme yap."),
    ("user", "Soru: {question}")
])

# CSS dosyasını yükle
try:
    with open("style.css", "r") as css_file:
        css = css_file.read()
except FileNotFoundError:
    css = ""

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Başlık
st.markdown('<div class="intro-text">Yapay Zeka Asistanınıza Hoş Geldiniz</div>', unsafe_allow_html=True)

# Sohbet geçmişi
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Mesaj gönderildi mi durumunu izlemek için
if 'message_processed' not in st.session_state:
    st.session_state.message_processed = False

# Model ayarları
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GEMINI_API_KEY, max_output_tokens=100)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Sohbet geçmişini göster
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{message["content"]}</div>', unsafe_allow_html=True)

# Mesaj giriş formu
with st.form(key="chat_form", clear_on_submit=True):
    input_text = st.text_input("Mesajınızı buraya yazın", key="input", placeholder="Mesajınızı buraya yazın...")
    submit_button = st.form_submit_button("Gönder")

# Form dışında işleme
if submit_button and input_text.strip() and not st.session_state.message_processed:
    st.session_state.message_processed = True  # İşlendi olarak işaretle
    st.session_state.chat_history.append({"role": "user", "content": input_text})

    try:
        response = chain.invoke({"question": input_text})
        st.session_state.chat_history.append({"role": "bot", "content": response})
    except Exception as e:
        st.session_state.chat_history.append({"role": "bot", "content": f"Bir hata oluştu: {str(e)}"})

    st.rerun()
else:
    # Form gönderme işlemi tamamlandıktan sonra durumu sıfırla
    st.session_state.message_processed = False