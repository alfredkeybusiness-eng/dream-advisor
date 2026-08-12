"""Database engine/session setup.

Defaults to a local SQLite file so the backend runs with zero setup in dev
(`uvicorn app.main:app`); Render sets DATABASE_URL to the provisioned
Postgres instance (see render.yaml), which takes over transparently --
the rest of the app talks to SQLAlchemy, not to a specific driver.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./dev.db")

# Render (and most managed Postgres providers) hand out `postgres://`, which
# SQLAlchemy's psycopg2 dialect no longer accepts -- normalize it.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
