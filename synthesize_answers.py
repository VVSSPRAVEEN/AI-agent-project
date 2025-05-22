from langchain.llms import OpenAI

def retrieve_and_synthesize(index, documents, question):
    embeddings_model = OpenAIEmbeddings()
    question_embedding = embeddings_model.embed_text(question)
    faiss.normalize_L2(np.array([question_embedding], dtype='float32'))
    distances, indices = index.search(np.array([question_embedding], dtype='float32'), k=3)

    context = " ".join([documents[idx][1] for idx in indices[0]])
    llm = OpenAI(model_name="gpt-3.5-turbo")
    response = llm.completion(prompt=f"Question: {question}\nContext: {context}\nAnswer:")
    return response