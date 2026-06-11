from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
def save_vector_store(vectorstore):
    vectorstore.save_local("faiss_index")
def load_vector_store():
    return FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=150,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " "
    ]
    )
    return splitter.split_documents(documents)


def create_vector_store(chunks):

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    save_vector_store(vectorstore)

    return vectorstore