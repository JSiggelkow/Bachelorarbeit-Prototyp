from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_core.tools import tool

from agent.config import get_model
from agent.middleware import PII_MIDDLEWARE, PromptInjectionGuardMiddleware
from agent.tools.user import create_user, get_user_by_id, find_user_by_name, find_user_by_email, delete_user, get_users

action_agent = create_agent(
    name="Aktionsagent",
    model=get_model(),
    tools=[create_user, get_users, get_user_by_id, find_user_by_name, find_user_by_email, delete_user],
    system_prompt=(
        "You manage user in the application database. "
        "Use the tools to create, retrieve, update, and delete users."
        "Always return the raw return value of the tool."
        "If a tool does not return any value, return 'DB access does not work'"
        "If tool usage got denied, return 'Tool usage got denied'"
    ),
    middleware=[
        PromptInjectionGuardMiddleware(),
        *PII_MIDDLEWARE,
        HumanInTheLoopMiddleware(
            interrupt_on={
                "create_user": {"allowed_decisions": ["approve", "reject"]},
                "delete_user": {"allowed_decisions": ["approve", "reject"]},
                "get_users": False,
                "get_user_by_id": False,
                "find_user_by_name": False,
                "find_user_by_email": False,
            },
            description_prefix="Freigabe erforderlich für folgende Aktion",
        )
    ],
)


@tool("database_agent")
def database_agent(request: str) -> str:
    """Agent to create, retrieve, or delete users in the application database.
        Needs certain arguments to work:
        create_user: name, email
        get_users: None
        get_user_by_id: user_id
        find_user_by_name: name
        find_user_by_email: email
        delete_user: user_id

        Before Using this tool, make sure you have the required arguments.
        Ask the user for them if they are not provided.
    """
    result = action_agent.invoke(
        {"messages": [{"role": "user", "content": request}]}
    )
    return result["messages"][-1].text
