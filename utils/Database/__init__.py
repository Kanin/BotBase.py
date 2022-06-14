import os

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_async_engine(os.getenv("DATABASE_URL"), future=True, echo=False)
async_session = scoped_session(sessionmaker(engine, expire_on_commit=False, class_=AsyncSession))

Base = declarative_base()
Base.query = async_session.query_property()
