from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi_cache.decorator import cache
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import apaginate

from crud.category.repository import CategoryRepository
from dependencies.crud import get_category_repository
from exceptions.database.integrity import HttpIntegrityError
from models.category.schemas import ReadCategory, CreateCategory

router = APIRouter(prefix="/category", tags=["Category"])


@router.get("/", response_model=Page[ReadCategory])
@cache(expire=3600, namespace="category-list")
async def get_all_sql(
    repo: Annotated["CategoryRepository", Depends(get_category_repository)],
    params: Params = Depends(),  # noqa Need for cache builder
):
    result = await apaginate(repo.session, repo.get_select_all())
    return result


@router.post("/", response_model=ReadCategory)
async def create_category(
    category_data: Annotated[CreateCategory, Form(media_type="multipart/form-data")],
    repo: Annotated["CategoryRepository", Depends(get_category_repository)],
):
    result = await repo.create_category(category_data)
    if not result:
        raise HttpIntegrityError()
    return result
