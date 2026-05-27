import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("textbook")

def load_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    words = full_text.split()
    chunks = [" ".join(words[i:i+300]) for i in range(0, len(words), 300)]

    collection.delete(where={"source": {"$ne": ""}}) if collection.count() > 0 else None

    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"chunk_{i}"],
            metadatas=[{"source": pdf_path}]
        )
    return len(chunks)

def search_context(query, n=3):
    if collection.count() == 0:
        return ""
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=n)
    return "\n\n".join(results["documents"][0])
