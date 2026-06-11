from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)
prompt = ChatPromptTemplate.from_template(
"""
You are an intelligent document assistant.

Answer ONLY using the provided context.

Guidelines:

- If information exists in the context, answer it.
- If information is spread across multiple chunks, combine it.
- If the user asks for explanation or summary, explain in your own words using the context.
- When listing items, include ALL items found.
- Do not invent information.

Only reply:

I could not find the answer in the uploaded document.

if the answer is genuinely absent from the context.

Context:
{context}

Question:
{question}

Answer:
"""
)

def generate_answer(context, question):

    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    return response.content