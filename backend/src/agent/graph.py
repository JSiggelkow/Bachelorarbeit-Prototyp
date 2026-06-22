from __future__ import annotations

from langchain.agents import create_agent

from agent.config import get_model
from agent.subagents.action import database_agent
from agent.subagents.knowledge import knowledge

graph = create_agent(
        model=get_model(),
        tools=[knowledge, database_agent],
        system_prompt="You are an supervisor Agent with you Tools as Child-Agents"
)

