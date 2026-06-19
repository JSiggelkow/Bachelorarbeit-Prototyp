from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def get_model() -> ChatOpenAI:
    return ChatOpenAI(model="gpt-5.5")