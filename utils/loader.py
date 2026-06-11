from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import CSVLoader


import os

def load_pdf(file_path):

    docs = PyPDFLoader(file_path).load()

    filename = os.path.basename(file_path)

    for doc in docs:
        doc.metadata["source_file"] = filename

    return docs


def load_csv(file_path):

    docs = CSVLoader(file_path=file_path).load()

    filename = os.path.basename(file_path)

    for doc in docs:
        doc.metadata["source_file"] = filename

    return docs

def load_document(file_path):

    if file_path.endswith(".pdf"):
        return load_pdf(file_path)

    elif file_path.endswith(".csv"):
        return load_csv(file_path)

    else:
        raise ValueError("Unsupported file type")