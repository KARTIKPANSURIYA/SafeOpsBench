"""Isolated database factory."""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from safeopsbench.db.base import Base


def create_database(
    url: str = "sqlite+pysqlite:///:memory:",
) -> tuple[Engine, sessionmaker[Session]]:
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    return engine, sessionmaker(engine, expire_on_commit=False)
