import asyncio
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient

from agent.config import get_model
from agent.middleware import PII_MIDDLEWARE, PromptInjectionGuardMiddleware, LLMInjectionGuardMiddleware

load_dotenv()


_client = MultiServerMCPClient(
    {
        "atlassian": {
            "transport": "http",
            "url": os.environ.get("ATLASSIAN_MCP_URL", "http://localhost:9000/mcp")
        }
    }
)

tools = asyncio.run(_client.get_tools())
print([t.name for t in tools])

_integration_agent = None

async def _build_integration_agent():
    tools = await _client.get_tools()
    return create_agent(
        name="Integrationsagent",
        model=get_model(),
        tools=tools,
        system_prompt=(
            "You are an Jira-Assistant. You are connected to a Jira-Project and you can manage it with Tools."
        ),
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "jira_create_issue": True,
                    "jira_update_issue": True,
                    "jira_delete_issue": True,
                    "jira_transition_issue": True,
                    "jira_search": False,
                    "jira_get_issue": False,
                },
                description_prefix="Freigabe erforderlich für folgende Aktion"
            )
        ]
    )

@tool("jira_agent")
async def jira_agent(request: str) -> str:
    """Agent to create, retrieve, or delete issues in the Jira Project"""
    global _integration_agent
    if not _integration_agent:
        _integration_agent = await _build_integration_agent()
    result = await _integration_agent.ainvoke({"messages": [{"role": "user", "content": request}]})
    return result["messages"][-1].text