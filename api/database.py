from _contextvars import ContextVar

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.server import app
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()
metadata = MetaData()

engine = create_async_engine(DATABASE_URL)
async_sessionmaker = sessionmaker(engine, AsyncSession, expire_on_commit=False)

_base_model_session_ctx = ContextVar("session")

# Регистрация промежуточного ПО
@app.middleware("request")
async def inject_session(request):
    request.ctx.session = async_sessionmaker()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)

@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()
