from langchain.agents import create_agent
from langchain.tools import tool

from agent.config import get_model
from agent.middleware import PII_MIDDLEWARE, PromptInjectionGuardMiddleware, LLMInjectionGuardMiddleware
from agent.vectorstore import get_vector_store

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
    middleware=[
        PromptInjectionGuardMiddleware(),
        LLMInjectionGuardMiddleware(),
        *PII_MIDDLEWARE,
    ],
)

@tool("knowledge")
def knowledge(request: str) -> str:
    """Answers Questions with knowledge"""
    result = knowledge_agent.invoke(
        {
            "messages": [{
                "role": "user",
                "content": request
            }]
        }
    )
    return result["messages"][-1].text