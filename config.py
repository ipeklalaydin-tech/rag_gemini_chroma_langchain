import os
from dotenv import load_dotenv

load_dotenv()

# Önce ortam değişkeni, yoksa Streamlit Secrets
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

try:
    import streamlit as st  # streamlit ortamında mevcut
    if not GOOGLE_API_KEY:
        GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")
except Exception:
    pass  # local çalışmada streamlit yoksa sorun değil

# Diğer ayarlar
DATA_DIR = "data"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 5
