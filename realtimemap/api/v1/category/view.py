from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from fastapi_pagination import Page, Params, paginate
from fastapi_pagination.ext.sqlalchemy import apaginate

from crud.category.repository import CategoryRepository
from dependencies.crud import get_category_repository
from models.category.schemas import ReadCategory

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/pg", response_model=Page[ReadCategory])
@cache(expire=3600)
async def get_category(
    repo: Annotated["CategoryRepository", Depends(get_category_repository)],
):
    result = await repo.get_all()
    return paginate(result)


@router.get("/", response_model=Page[ReadCategory])
@cache(expire=3600, namespace="category-list")
async def get_all_sql(
    repo: Annotated["CategoryRepository", Depends(get_category_repository)],
    params: Params = Depends(),  # Need for cache in Redis mb FIX
):
    return await apaginate(repo.session, repo.get_select_all())
