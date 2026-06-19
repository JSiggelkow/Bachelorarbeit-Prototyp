from langchain.agents import create_agent
from langchain.tools import tool

from agent.config import get_model

knowledge_agent = create_agent(
    name="Wissensagent",
    model=get_model(),
    system_prompt="You just return: 'Wissensagent funktioniert'",
)

@tool("knowledge")
def knowledge(request: str) -> str:
    """Answers Questions has knowledge"""
    result = knowledge_agent.invoke(
        {
            "messages": [{
                "role": "user",
                "content": request
            }]
        }
    )
    return result["messages"][-1].text