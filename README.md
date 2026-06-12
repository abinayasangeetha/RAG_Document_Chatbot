# 📄 RAG Document Chatbot

## Overview

RAG Document Chatbot is an AI-powered application that allows users to upload PDF documents and CSV datasets, then interact with them using natural language questions.

The project combines:

- Retrieval-Augmented Generation (RAG) for PDF Question Answering
- Pandas-based Query Engine for CSV Analysis
- FAISS Vector Database
- HuggingFace Embeddings
- Groq Llama 3.3 70B
- Streamlit User Interface

The system supports multiple PDF and CSV uploads simultaneously and automatically routes questions to the appropriate processing pipeline.

---

## Features

### 📑 PDF Question Answering

- Upload one or more PDF files
- Ask questions about document content
- Summarize reports and documents
- Extract project details, skills, technologies, objectives, etc.

### 📊 CSV Dataset Analysis

- Upload one or more CSV datasets
- Retrieve exact values
- Calculate averages
- Find minimum and maximum values
- Count rows and columns
- Display column names
- View missing values
- Generate dataset summaries

### 📂 Multi-Document Support

Supports:

- Multiple PDFs
- Multiple CSVs
- Mixed PDF and CSV uploads

---

## Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend |
| Streamlit | User Interface |
| LangChain | RAG Pipeline |
| HuggingFace Embeddings | Text Embeddings |
| FAISS | Vector Database |
| Groq Llama 3.3 70B | Answer Generation |
| Pandas | CSV Processing |

---

# System Architecture

```text
                        ┌─────────────────┐
                        │ User Uploads    │
                        │ PDF / CSV Files │
                        └────────┬────────┘
                                 │
                                 ▼
                     ┌─────────────────────┐
                     │      app.py         │
                     │ Main Controller     │
                     └───────┬─────────────┘
                             │
            ┌────────────────┴───────────────┐
            │                                │
            ▼                                ▼

    PDF PIPELINE                      CSV PIPELINE

┌─────────────────┐          ┌────────────────────┐
│   loader.py     │          │   csv_handler.py   │
│ Load PDF Files  │          │ Store DataFrames   │
└────────┬────────┘          └─────────┬──────────┘
         │                              │
         ▼                              ▼

┌─────────────────┐          ┌────────────────────┐
│ vector_store.py │          │ query_router.py    │
│ Chunking        │          │ Route CSV Queries  │
│ Embeddings      │          └─────────┬──────────┘
│ FAISS Storage   │                    │
└────────┬────────┘                    ▼
         │                    ┌────────────────────┐
         ▼                    │ csv_agent.py       │
                              │ Query Parsing      │
┌─────────────────┐           └─────────┬──────────┘
│ retriever.py    │                     │
│ Similarity      │                     ▼
│ Search          │           ┌────────────────────┐
└────────┬────────┘           │ csv_query_engine.py│
         │                    │ Pandas Execution   │
         ▼                    └─────────┬──────────┘
                                        │
┌─────────────────┐                     ▼
│ rag_chain.py    │            Exact Dataset Answer
│ Groq LLM        │
└────────┬────────┘
         │
         ▼

 Document-Based Answer
```

---

# PDF Workflow

### Step 1: Upload PDF

User uploads one or more PDF files.

### Step 2: Document Loading

`loader.py`

Uses:

```python
PyPDFLoader
```

to extract text from PDF pages.

### Step 3: Chunking

`vector_store.py`

Uses:

```python
RecursiveCharacterTextSplitter
```

to divide large documents into manageable chunks.

### Step 4: Embedding Generation

Uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

to convert chunks into vector embeddings.

### Step 5: FAISS Storage

Embeddings are stored in the FAISS vector database.

### Step 6: User Query

User asks a question.

### Step 7: Retrieval

`retriever.py`

Retrieves the most relevant chunks using similarity search.

### Step 8: Answer Generation

`rag_chain.py`

Sends:

- Retrieved Context
- User Question

to Groq Llama 3.3 70B.

### Step 9: Final Response

The model generates an answer based only on retrieved document content.

---

# CSV Workflow

### Step 1: Upload CSV

User uploads one or more CSV datasets.

### Step 2: Data Loading

`csv_handler.py`

Uses:

```python
pd.read_csv()
```

to load datasets into Pandas DataFrames.

Example:

```python
{
    "Mall_Customers.csv": df1,
    "taxi_trip_pricing.csv": df2
}
```

### Step 3: Query Routing

`query_router.py`

Determines whether the question belongs to CSV analysis.

### Step 4: Query Understanding

`csv_agent.py`

Converts natural language questions into structured instructions.

Example:

```python
{
    "operation": "lookup",
    "target_column": "Age",
    "filter_column": "CustomerID",
    "filter_value": 10
}
```

### Step 5: Query Execution

`csv_query_engine.py`

Executes the corresponding Pandas operation.

Example:

```python
df[df["CustomerID"] == 10]
```

### Step 6: Exact Answer

Returns precise values directly from the dataset.

---

# Models Used

## 1. HuggingFace Embedding Model

Model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Purpose:

- Convert text into numerical vectors
- Enable semantic similarity search

---

## 2. FAISS

Purpose:

- Store vector embeddings
- Perform fast similarity retrieval

---

## 3. Groq Llama 3.3 70B

Model:

```text
llama-3.3-70b-versatile
```

Purpose:

- Understand retrieved context
- Generate natural language answers

---

# Advantages

✅ Supports Multiple PDFs

✅ Supports Multiple CSV Datasets

✅ Fast Semantic Search

✅ Exact Dataset Retrieval

✅ Natural Language Interface

✅ Reduced Hallucination using RAG

✅ Easy for Non-Technical Users

---

# Limitations

## PDF Retrieval Limitation

Only Top-K chunks are retrieved.

Sometimes relevant information may exist outside retrieved chunks.

### Solution

- Increase Top-K
- Use Hybrid Search
- Use Reranking Models

---

## Large PDF Limitation

Large PDFs generate many chunks.

This increases:

- Storage
- Retrieval Time

### Solution

- Better Chunking Strategies
- Metadata Filtering
- Hybrid Retrieval

---

## CSV Query Limitation

Currently optimized for:

- Lookups
- Mean
- Min
- Max
- Summary Statistics

Complex analytical queries may require advanced agents.

### Solution

- Pandas AI
- LangChain DataFrame Agents
- SQL Query Engine

---

# Future Enhancements

- Hybrid Search (Keyword + Semantic Search)
- Reranking Models
- Conversational Memory
- Automatic Data Visualization
- SQL Database Support
- Advanced Data Analytics Agent

---

# Project Structure

```text
RAG_Document_Chatbot/
│
├── app.py
│
├── utils/
│   ├── loader.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── rag_chain.py
│   ├── csv_handler.py
│   ├── query_router.py
│   ├── csv_agent.py
│   └── csv_query_engine.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Sample Questions

## PDF Questions

```text
What is the project title?

Who is the supervisor?

Summarize the project.

What technologies are used?
```

## CSV Questions

```text
How many rows?

How many columns?

What is average Trip_Price?

What is maximum Spending Score?

What is Age of CustomerID 10?
```

---

# Conclusion

This project demonstrates the integration of Retrieval-Augmented Generation (RAG) and structured data analysis within a single intelligent application.

By combining:

- FAISS Vector Database
- HuggingFace Embeddings
- Groq Llama 3.3 70B
- Pandas Query Engine
- Streamlit

the chatbot enables users to interact with documents and datasets using natural language, making information retrieval and data analysis faster, more intuitive, and accessible.
