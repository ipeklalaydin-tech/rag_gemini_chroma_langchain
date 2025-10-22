import os
from dotenv import load_dotenv
load_dotenv()

# 1) Önce ortam değişkenini dene
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 2) Streamlit'te ise secrets'tan oku (env yoksa)
try:
    import streamlit as st
    if not GOOGLE_API_KEY:
        GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")
except Exception:
    pass

# Ayarlar
DATA_DIR = "data"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 5
