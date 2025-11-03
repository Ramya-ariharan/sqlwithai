

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import text, create_engine
from model_selector import get_model_client
import re

app = FastAPI(title="🧠 QueryMaker API", version="1.1")

# --- Database setup ---
DATABASE_URL = "sqlite:///./querymaker.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# --- Request Model ---
class QueryRequest(BaseModel):
    question: str
    provider: str = "openai"  # or "groq"

@app.get("/")
def root():
    return {"message": "🚀 QueryMaker API running successfully!"}

@app.post("/query")
def generate_and_execute_query(request: QueryRequest):
    client, model_name = get_model_client(request.provider)

    prompt = f"""
    You are an expert SQL query generator.
    For this question: "{request.question}"

    Generate ONLY a valid SQL query for a SQLite database that has a table named 'customers'
    with columns: id (int), name (text), email (text), country (text), total_purchases (float).

    STRICT RULES:
    - Do NOT explain the query.
    - Do NOT include markdown, code blocks, or text like 'Here is your query'.
    - Return ONLY the SQL query itself.
    """

    try:
        # --- AI call ---
        if request.provider == "openai":
            ai_response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a SQL expert that outputs ONLY valid SQL queries."},
                    {"role": "user", "content": prompt}
                ]
            )
            sql_query = ai_response.choices[0].message.content.strip()
        else:
            ai_response = client.invoke(prompt)
            sql_query = ai_response.content if hasattr(ai_response, "content") else str(ai_response)

        # --- Clean the response ---
        sql_query = re.sub(r"```sql|```", "", sql_query).strip()

    except Exception as e:
        return {"error": f"AI model error: {str(e)}"}

    # --- Execute the query safely ---
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return {"error": f"SQL execution error: {str(e)}", "sql_query": sql_query}

    return {"sql_query": sql_query, "data": data}
