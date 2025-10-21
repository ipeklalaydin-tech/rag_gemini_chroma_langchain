from typing import List, Tuple
from jinja2 import Template

# Haystack 2 bileşenleri
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.writers import DocumentWriter
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.dataclasses import Document

import google.generativeai as genai
import config

# --- Gemini ayarı ---
genai.configure(api_key=config.GOOGLE_API_KEY)

def gemini_generate(prompt: str) -> str:
    """Gemini gemini-2.0-flash-001 ile kısa cevap üret."""
    model = genai.GenerativeModel("gemini-2.0-flash-001")
    # alternatif: genai.GenerativeModel("gemini-1.5-flash-001")
    resp = model.generate_content(prompt)
    return (resp.text or "").strip()

def build_index(docs: List[dict]):
    """InMemory store + BM25 retriever kur, verileri yaz."""
    store = InMemoryDocumentStore()
    writer = DocumentWriter(document_store=store)
    writer.run([Document(content=d["content"]) for d in docs])
    retriever = InMemoryBM25Retriever(document_store=store, top_k=config.TOP_K)
    return store, retriever

PROMPT_TEMPLATE = """Aşağıda kullanıcı sorusu ve ilgili kaynak parçaları var.
Kaynaklara sadık kalarak Türkçe, kısa ve anlaşılır cevap ver. Gerekirse maddeler kullan.

Soru:
{{ question }}

Kaynak Parçalar:
{% for d in documents %}
- {{ d.content }}
{% endfor %}
"""

def build_rag_answer(question: str, retriever) -> Tuple[str, List[Document]]:
    """Sorgula, promptu kur, Gemini'den yanıt al, (yanıt, dönen dokümanlar) döndür."""
    retrieved = retriever.run(query=question)
    docs: List[Document] = retrieved["documents"]

    t = Template(PROMPT_TEMPLATE)
    prompt = t.render(question=question, documents=docs)

    answer = gemini_generate(prompt)
    return answer, docs
