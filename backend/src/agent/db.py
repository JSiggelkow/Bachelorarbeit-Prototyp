from __future__ import annotations
import os

from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

engine = create_engine(os.environ['DATABASE_URL'])

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True)

def init_db() -> None:
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    print("Db created")