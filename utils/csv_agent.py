from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def get_csv_instruction(
    question,
    columns
):

    prompt = f"""
You are a CSV Data Analyst.

Available Columns:
{columns}

Convert the question into JSON.

Operations:

lookup
average
maximum
minimum
count_rows
count_columns
column_names
missing_values
describe

Examples:

Question:
What is Age of CustomerID 10?

Output:
{{
    "operation":"lookup",
    "target_column":"Age",
    "filter_column":"CustomerID",
    "filter_value":"10"
}}

Question:
What is average Trip_Price?

Output:
{{
    "operation":"average",
    "target_column":"Trip_Price"
}}

Question:
How many rows?

Output:
{{
    "operation":"count_rows"
}}

Question:
Show column names

Output:
{{
    "operation":"column_names"
}}

Return ONLY valid JSON.

Question:
{question}
"""

    response = llm.invoke(prompt)

    try:
        return json.loads(response.content)

    except:
        return None