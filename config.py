import os
from dotenv import load_dotenv

load_dotenv()

# Önce environment değişkenini dene
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Streamlit ortamı için fallback
try:
    import streamlit as st
    if not GOOGLE_API_KEY:
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    pass

# Diğer ayarlar
DATA_DIR = "data"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 5
