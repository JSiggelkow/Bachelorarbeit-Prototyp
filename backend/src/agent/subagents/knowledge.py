from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy
from langchain.tools import tool
from pydantic import BaseModel, Field

from agent.config import get_model
from agent.middleware import ToolResultInjectionGuardMiddleware
from agent.vectorstore import get_vector_store


class Source(BaseModel):

    content: str = Field(description="The content of the source")
    metadata: dict = Field(description="The metadata of the source")


class KnowledgeResponse(BaseModel):
    response: str = Field(description="The response. 'Knowledge not found', if nothing was found.")
    sources: list[Source] = Field(
        default_factory=list,
        description="All sources that were used to answer the question.",
    )

@tool(response_format="content_and_artifact")
def retrieve_knowledge(query: str):
    """Searches for knowledge in the vectorstore"""
    docs = get_vector_store().similarity_search(query, k=4)
    serialized = "\n\n".join(
        f"Source: {d.metadata}\nContent: {d.page_content}" for d in docs
    )
    return serialized, docs

knowledge_agent = create_agent(
    name="Wissensagent",
    model=get_model(),
    tools=[retrieve_knowledge],
    system_prompt="Always use the retrieve_knowledge tool before Answering. If you cannot find the answer in the retrieved knowledge, answer with 'Knowledge not found'",
    response_format=ProviderStrategy(KnowledgeResponse),
    middleware=[
        ToolResultInjectionGuardMiddleware(),
    ]
)
@tool("knowledge")
async def knowledge(request: str) -> str:
    """Answers questions about internal documents, including source references."""
    result = await knowledge_agent.ainvoke(
        {"messages": [{"role": "user", "content": request}]}
    )
    response: KnowledgeResponse = result["structured_response"]

    if not response.sources:
        return response.response

    quellen_text = "\n".join(
        f"- {q.metadata.get('source', 'unbekannt')}" for q in response.sources
    )
    return f"{response.response}\n\nQuellen:\n{quellen_text}"
