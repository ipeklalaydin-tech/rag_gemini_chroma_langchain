import os
import streamlit as st

st.set_page_config(page_title="RAG Gemini Chroma", layout="wide")
st.title("RAG + Gemini + Chroma (Demo)")
st.write("✅ App boot başladı")

# --- 1) Secrets / Env kontrolü ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY bulunamadı. Streamlit → App settings → Secrets kısmına ekleyin.")
    st.stop()

# --- 2) Ağır import'lar korumalı ---
try:
    import google.generativeai as genai
    genai.configure(api_key=GOOGLE_API_KEY)
    st.write("✅ Google GenAI hazır")
except Exception as e:
    st.exception(e)
    st.stop()

# (Opsiyonel) Vektör DB / Chroma başlangıcı (ileride kullanacaksan)
@st.cache_resource(show_spinner="Vektör veritabanı hazırlanıyor...")
def get_vector_store():
    # from chromadb import PersistentClient
    # return PersistentClient(path="chroma_db")
    return "OK"  # şimdilik placeholder

try:
    vs = get_vector_store()
    st.write("✅ Vektör veritabanı hazır")
except Exception as e:
    st.exception(e)
    st.stop()

# --- 3) Basit arayüz: Gemini ile soru-cevap ---
st.subheader("Hızlı Soru-Cevap (Gemini)")

default_prompt = "Merhaba! Bu bir sağlık kontrolü sorusu. Kısaca yanıt verir misin?"
user_prompt = st.text_area("Sorunuzu yazın:", value=default_prompt, height=120)
model_name = st.selectbox("Model", ["gemini-1.5-flash", "gemini-1.5-pro"], index=0)

if st.button("Çalıştır"):
    try:
        model = genai.GenerativeModel(model_name=model_name)
        resp = model.generate_content(user_prompt)
        st.success("✅ Yanıt alındı")
        st.write(resp.text if hasattr(resp, "text") else resp)
    except Exception as e:
        st.error("İstek sırasında hata oluştu:")
        st.exception(e)

st.caption("Not: RAG tarafını (Chroma/Haystack) adım adım ekleyebiliriz; bu iskelet, önce uygulamanın stabil açıldığını doğrulamak içindir.")
