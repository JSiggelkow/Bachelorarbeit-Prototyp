from langchain_core.tools import tool
from sqlalchemy import select
from sqlalchemy.orm import Session

from agent.db import engine, User


@tool
def create_user(name: str, email: str) -> str:
    """Creates a new user with the given name and email."""
    with Session(engine) as session:
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        return f"User {name} created with email {email} and with ID {user.id}."

@tool
def get_users() -> str:
    """Returns a list of all users."""
    with Session(engine) as session:
        users = session.scalars(select(User)).all()
        if not users:
            return "No users found."
        return "\n".join([f"{user.name} ({user.email})" for user in users])

@tool
def get_user_by_id(user_id: int) -> str:
    """Returns the user with the given ID."""
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            return f"User with ID {user_id} not found."
        return f"name: {user.name}, email: {user.email}, id: {user.id}"

@tool
def find_user_by_name(name: str) -> str:
    """Returns the users with the given name."""
    with Session(engine) as session:
        users = session.scalars(select(User).where(User.name == name)).all()
        if not users:
            return f"No users found with name {name}."
        return "\n".join([f"name: {user.name}, email: {user.email}, id: {user.id}" for user in users])

@tool
def find_user_by_email(email: str) -> str:
    """Returns the user with the given email"""
    with Session(engine) as session:
        user = session.scalar(select(User).where(User.email == email))
        if not user:
            return f"No user found with email {email}."
        return f"name: {user.name}, email: {user.email}, id: {user.id}"

@tool
def delete_user(user_id: int) -> str:
    """Deletes the user with the given ID."""
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            return f"User with ID {user_id} not found."
        session.delete(user)
        session.commit()
        return f"User with ID {user_id} deleted."

