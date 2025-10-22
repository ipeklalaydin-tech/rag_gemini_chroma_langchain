import os
import streamlit as st

st.set_page_config(page_title="RAG Gemini Chroma", layout="wide")
st.title("Soru Cevaplama Arayüzü")

# --- 1) Secrets / Env kontrolü ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY bulunamadı. Streamlit → App settings → Secrets kısmına ekleyin.")
    st.stop()

# --- 2) Google GenAI init ---
try:
    import google.generativeai as genai
    genai.configure(api_key=GOOGLE_API_KEY)
    
except Exception as e:
    st.exception(e)
    st.stop()

# --- 3) Destekli modelleri listele (generateContent destekleyenler) ---
@st.cache_resource(show_spinner="Modeller alınıyor…")
def get_supported_models():
    try:
        models = genai.list_models()
        ok = []
        for m in models:
            methods = getattr(m, "supported_generation_methods", []) or []
            if "generateContent" in methods:
                # m.name genelde "models/gemini-2.0-flash-001" şeklindedir
                clean = m.name.split("/", 1)[-1]
                ok.append(clean)
        # Yaygın tercihleri başa al
        preferred_order = [
            "gemini-2.0-flash-001",
            "gemini-2.0-pro-exp-02-05",  # varsa
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b",
        ]
        # unique ve sıralı birleşim
        seen = set()
        ordered = []
        for p in preferred_order + ok:
            if p not in seen and p in ok:
                seen.add(p)
                ordered.append(p)
        return ordered or ok
    except Exception:
        # Listeleme başarısızsa yine de bilinen isimleri deneriz
        return ["gemini-2.0-flash-001", "gemini-1.5-flash", "gemini-1.5-pro"]

supported_models = get_supported_models()

# Varsayılanı gemini-2.0-flash-001 yap
DEFAULT_MODEL = "gemini-2.0-flash-001"
if DEFAULT_MODEL not in supported_models and supported_models:
    DEFAULT_MODEL = supported_models[0]

# --- 4) (Opsiyonel) Vektör DB / Chroma placeholder ---
@st.cache_resource(show_spinner="Vektör veritabanı hazırlanıyor...")
def get_vector_store():
    # from chromadb import PersistentClient
    # return PersistentClient(path="chroma_db")
    return "OK"  # şimdilik placeholder

try:
    vs = get_vector_store()
    
except Exception as e:
    st.exception(e)
    st.stop()

# --- 5) Arayüz ---
st.subheader("Soru Cevap")
default_prompt = "Projify projesi ile ilgili sorunuzu sorun. "
user_prompt = st.text_area("Sorunuzu yazın:", value=default_prompt, height=120)

col1, col2 = st.columns([2,1])
with col1:
    model_name = st.selectbox("Model", supported_models, index=max(0, supported_models.index(DEFAULT_MODEL)) if DEFAULT_MODEL in supported_models else 0)
with col2:
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)

# İstenmeden "models/..." girilirse temizle
def normalize_model_id(name: str) -> str:
    return (name or "").split("/", 1)[-1]

if st.button("Çalıştır"):
    try:
        target_model = normalize_model_id(model_name)
        model = genai.GenerativeModel(model_name=target_model)
        resp = model.generate_content(
            user_prompt,
            generation_config={
                "temperature": temperature,
            },
        )
        st.success(f"✅ Yanıt alındı ({target_model})")
        st.write(resp.text if hasattr(resp, "text") else resp)
    except Exception as e:
        st.error("İstek sırasında hata oluştu:")
        st.exception(e)

st.caption("Not: RAG tarafını (Chroma/Haystack) adım adım ekleyebiliriz; bu iskelet, önce uygulamanın stabil açıldığını doğrulamak içindir.")

