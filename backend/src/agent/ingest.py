from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

load_dotenv()

from agent.vectorstore import get_vector_store

def ingest(docs: list[Document]) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    return get_vector_store().add_documents(chunks)

##Just an example because file upload does not exist yet!
if __name__ == "__main__":
    sample = [Document(page_content="Die IKS hat ihren Sitz in Hilden, wurde 1989 gegründet und hat 85 IT-Berater. Ihr Geschäftsführer ist Hartwig Tödter.")]
    print(ingest(sample))