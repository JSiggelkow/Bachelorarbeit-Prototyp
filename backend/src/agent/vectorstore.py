import os

from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

COLLECTION = "knowledge_base"

def get_vector_store() -> PGVector:
    return PGVector(
        embeddings=OpenAIEmbeddings(model="text-embedding-3-large"),
        collection_name=COLLECTION,
        connection=os.environ["DATABASE_URL"],
        use_jsonb=True,
    )