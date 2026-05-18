import os
import sys

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends

from models import *

from dotenv import load_dotenv

load_dotenv()

connect_url = os.getenv("DATABASE_URL")

if connect_url is None:
    raise Exception("No database url provided.")

URL_DATABASE = DATABASE_URL = connect_url

engine = create_async_engine(URL_DATABASE, echo=False)

async_session_maker = async_sessionmaker(
    engine,
    #class_=AsyncSession,
    expire_on_commit=False
)

async def init_models():
    
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)
        ...


async def get_session():
    session = async_session_maker()
    
    try:
        yield session
        await session.commit()

    except Exception as e:
        await session.rollback()
        raise e
    
    finally:
        await session.close()


db_dependency = Annotated[AsyncSession, Depends(get_session)]