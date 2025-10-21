import os
from typing import List, Dict
import config

def load_local_texts() -> List[str]:
    """DATA_DIR altındaki .txt ve .md dosyalarını okuyup döndürür."""
    texts: List[str] = []
    if not os.path.isdir(config.DATA_DIR):
        return texts

    for root, _, files in os.walk(config.DATA_DIR):
        for f in files:
            if f.lower().endswith((".txt", ".md")):
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                    content = fh.read().strip()
                    if content:
                        texts.append(content)
    return texts

def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Sabit uzunlukta parçalar üretir (overlap’lı)."""
    chunks, start = [], 0 
    step = max(1, chunk_size - overlap)
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += step
    return chunks

def build_documents() -> List[Dict]:
    """Haystack Document’lerine benzer dict listesi döner: {'content': ...}"""
    docs: List[Dict] = []
    for t in load_local_texts():
        for ch in chunk_text(t, config.CHUNK_SIZE, config.CHUNK_OVERLAP):
            docs.append({"content": ch})
    return docs