import requests
import faiss
import numpy as np
import time
from config import GEMINI_API_KEY

cache = {}

def call_gemini_api(prompt):
    api_key = GEMINI_API_KEY
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}

    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    result = response.json()
    generated_text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

    print("DEBUG: Generated Text:", generated_text)  # Debugging
    return generated_text

def call_gemini_with_backoff(api_call, retries=5):
    for i in range(retries):
        try:
            return api_call()
        except Exception as e:
            if "rate limit" in str(e).lower() and i < retries - 1:
                time.sleep(2 ** i)
            else:
                raise

def create_embeddings(documents):
    document_texts = [doc[1] for doc in documents]
    embeddings = [len(text) for text in document_texts]  # Dummy logic
    return np.array(embeddings, dtype='float32')

def store_embeddings(embedding_matrix):
    dimension = 1
    index = faiss.IndexFlatL2(dimension)
    embedding_matrix = embedding_matrix.reshape(-1, 1)
    faiss.normalize_L2(embedding_matrix)
    index.add(embedding_matrix)
    return index

def retrieve_similar_documents(index, question_embedding, documents, k=3):
    faiss.normalize_L2(np.array([question_embedding], dtype='float32').reshape(1, -1))
    distances, indices = index.search(np.array([question_embedding], dtype='float32').reshape(1, -1), k)
    return [documents[idx][1] for idx in indices[0]]

def get_question_embedding(question):
    return np.array([len(question)], dtype='float32')