import streamlit as st
from document_ingestion import ingest_documents
from embeddings import (
    create_embeddings,
    store_embeddings,
    retrieve_similar_documents,
    get_question_embedding,
    call_gemini_with_backoff,
    call_gemini_api
)

def main():
    st.title("AI Document Assistant")
    file_paths = [
        r'C:\Users\varah\OneDrive\Desktop\kgen.txt',
        r"C:\Users\varah\OneDrive\Desktop\Loan Default case study-PPT.pdf",
        r"C:\Users\varah\OneDrive\Desktop\DataScienceInterviewQuestions.pdf"
    ]
    documents = ingest_documents(file_paths)
    embeddings = create_embeddings(documents)
    index = store_embeddings(embeddings)

    # Display the file names
    file_names = [file_path.split("\\")[-1] for file_path in file_paths]
    st.write("Files Read:", ", ".join(file_names))

    user_question = st.text_input("Enter your question:")
    if user_question:
        question_embedding = get_question_embedding(user_question)
        context_documents = retrieve_similar_documents(index, question_embedding, documents)
        response = retrieve_and_generate(user_question, context_documents)
        
        if response:
            st.write("Response:", response)
        else:
            st.write("No response generated. Please try another question.")

def retrieve_and_generate(question, context):
    full_context = question + " " + " ".join(context)

    def api_call():
        return call_gemini_api(full_context)

    generated_text = call_gemini_with_backoff(api_call)
    return generated_text

if __name__ == "__main__":
    main()