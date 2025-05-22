import fitz  # PyMuPDF

def read_pdf(file_path):
    with fitz.open(file_path) as doc:
        return "".join(page.get_text() for page in doc)

def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def ingest_documents(file_paths):
    documents = []
    for file_path in file_paths:
        text = read_pdf(file_path) if file_path.endswith('.pdf') else read_txt(file_path)
        documents.append((file_path, text))
    return documents