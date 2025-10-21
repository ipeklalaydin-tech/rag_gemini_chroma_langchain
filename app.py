import streamlit as st
from data_processing import build_documents
from rag_pipeline import build_index, build_rag_answer

st.set_page_config(page_title="Türkçe RAG Chatbot", layout="wide")
st.title("🇹🇷 RAG Chatbot (Gemini + Haystack)")

@st.cache_resource(show_spinner=True)
def get_retriever():
    docs = build_documents()
    _, retriever = build_index(docs)
    return retriever

with st.sidebar:
    st.header("Ayarlar")
    st.caption("İlk çalıştırmada 'data/' klasörü okunur, metinler parçalara bölünür ve indekslenir.")
    if st.button("Önbelleği temizle"):
        st.cache_resource.clear()
        st.rerun()

retriever = get_retriever()

q = st.text_input("Sorunu yaz (ör. 'Yapay zekâ nedir?')", "")
if st.button("Sor!") and q.strip():
    with st.spinner("Aranıyor ve yanıt hazırlanıyor..."):
        answer, docs = build_rag_answer(q.strip(), retriever)
    st.subheader("Yanıt")
    st.write(answer)
    with st.expander("Kaynak Parçalar"):
        for i, d in enumerate(docs, start=1):
            st.markdown(f"**{i}. Parça**")
            st.write(d.content)
else:
    st.info("🔎 Başlamak için sol tarafta `data/` klasörüne en az bir `.txt` veya `.md` dosyası koy, sonra bir soru sor.")
