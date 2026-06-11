import os
import tempfile
import streamlit as st

from utils.loader import load_document
from utils.vector_store import (
    split_documents,
    create_vector_store
)
from utils.retriever import retrieve_context
from utils.rag_chain import generate_answer
from utils.csv_handler import (
    csv_dataframes,
    store_csv
)

from utils.csv_query_engine import (
    answer_csv_question
)

from utils.query_router import (
    is_csv_query
)

st.set_page_config(
    page_title="RAG Document Chatbot",
    layout="wide"
)

# Session State
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "total_documents" not in st.session_state:
    st.session_state.total_documents = 0

if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0

st.title("📄 RAG Document Chatbot")

with st.sidebar:

    st.header("⚙️ Settings")

    top_k = st.slider(
        "Retrieved Chunks",
        1,
        20,
        10
    )

    show_sources = st.checkbox(
        "Show Sources",
        value=True
    )

    st.divider()

    st.subheader("📊 System Info")

    st.write(
        f"Documents: {st.session_state.total_documents}"
    )

    st.write(
        f"Chunks: {st.session_state.total_chunks}"
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

uploaded_files = st.file_uploader(
    "Upload Documents",
    type=["pdf", "csv"],
    accept_multiple_files=True
)

if uploaded_files:

    all_docs = []

    with st.spinner("Processing Documents..."):
        from utils.csv_handler import (
        csv_dataframes
           )

        csv_dataframes.clear()
        for uploaded_file in uploaded_files:

            suffix = os.path.splitext(
                uploaded_file.name
            )[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as tmp_file:

                tmp_file.write(
                    uploaded_file.read()
                )

                temp_path = tmp_file.name

            

            if uploaded_file.name.endswith(".csv"):

                     store_csv(
                     uploaded_file.name,
                          temp_path
                            )

            docs = load_document(
                   temp_path
                            )

            all_docs.extend(docs)

        chunks = split_documents(
            all_docs
        )

        st.session_state.total_documents = (
            len(uploaded_files)
        )

        st.session_state.total_chunks = (
            len(chunks)
        )

        vectorstore = create_vector_store(
            chunks
        )

        st.session_state.vectorstore = (
            vectorstore
        )

    st.success(
        f"Processed {len(uploaded_files)} file(s)"
    )

# Display Existing Chat
for chat in st.session_state.chat_history:

    with st.chat_message("user"):
        st.write(chat["question"])

    with st.chat_message("assistant"):
        st.write(chat["answer"])

question = st.chat_input(
    "Ask a question..."
)

if (
    question
    and (
        st.session_state.vectorstore
        or csv_dataframes
    )
):

    with st.chat_message("user"):
        st.write(question)

    if is_csv_query(question):

        answer = (
            answer_csv_question(
                question,
                csv_dataframes
            )
        )

        with st.chat_message(
            "assistant"
        ):
            st.write(answer)

    else:

        context, retrieved_docs = (
            retrieve_context(
                st.session_state.vectorstore,
                question,
                k=top_k
            )
        )

        answer = generate_answer(
            context=context,
            question=question
        )

        with st.chat_message(
            "assistant"
        ):

            st.write(answer)

            if (
                show_sources
                and retrieved_docs
            ):

                for i, doc in enumerate(
                    retrieved_docs
                ):

                    with st.expander(
                        f"Source Chunk {i+1}"
                    ):

                        st.write(
                            doc.page_content
                        )

    st.session_state.chat_history.append(
        {
            "question": question,
            "answer": answer
        }
    )