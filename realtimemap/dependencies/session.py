from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.helper import db_helper

get_session = Annotated[AsyncSession, Depends(db_helper.session_getter)]

context_get_session = asynccontextmanager(db_helper.session_getter)
