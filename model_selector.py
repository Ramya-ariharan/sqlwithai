import os
from openai import OpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pathlib import Path

# --- Load .env ---
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        f"🚨 OPENAI_API_KEY not found in {env_path}\n"
        "Please add it as: OPENAI_API_KEY=sk-xxxxxxyourkeyxxxxx"
    )

# --- Create the OpenAI client ---
openai_client = OpenAI(api_key=api_key)
groq_client = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant" ,
    streaming=True # or "mixtral-8x7b" depending on your need
)



def get_model_client(provider: str):
    """
    Returns both the model client and the model name for the given provider.
    """
    provider = provider.lower()

    if provider == "openai":
        # ✅ Return tuple (client, model_name)
        return openai_client, "gpt-4o-mini"

    # You can easily extend this later for Groq, Gemini, etc.
    elif provider == "groq":
        # llm=ChatGroq(groq_api_key=api_key,model_name="llama-3.1-8b-instant",streaming=True)
        # raise 
        return groq_client, 'llama-3.1-8b-instant'

    else:
        raise ValueError(f"❌ Unsupported provider: {provider}")
