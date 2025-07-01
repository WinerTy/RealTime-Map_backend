from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi_cache.decorator import cache
from fastapi_pagination import Page, Params, paginate
from fastapi_pagination.ext.sqlalchemy import apaginate
from starlette.requests import Request

from crud.category.repository import CategoryRepository
from dependencies.crud import get_category_repository
from models.category.schemas import ReadCategory, CreateCategory

router = APIRouter(prefix="/category", tags=["Category"])


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
    request: Request,
    repo: Annotated["CategoryRepository", Depends(get_category_repository)],
    params: Params = Depends(),
):
    result = await apaginate(repo.session, repo.get_select_all())
    return result


@router.post("/", response_model=ReadCategory)
async def create_category(
    category_data: Annotated[CreateCategory, Form(media_type="multipart/form-data")],
    repo: Annotated["CategoryRepository", Depends(get_category_repository)],
):
    result = await repo.create(category_data)
    return result
