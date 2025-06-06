from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi_cache.decorator import cache
from fastapi_pagination import Page, Params, paginate
from fastapi_pagination.ext.sqlalchemy import apaginate
from pydantic import BaseModel
from starlette.requests import Request

from crud.category.repository import CategoryRepository
from dependencies.crud import get_category_repository
from models.category.schemas import ReadCategory, CreateCategory

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/pg", response_model=Page[ReadCategory])
@cache(expire=3600)
async def get_category(
    repo: Annotated["CategoryRepository", Depends(get_category_repository)],
):
    result = await repo.get_all()
    return paginate(result)


class DebugCategoryRead(BaseModel):
    id: int
    icon: str


@router.get("/{category_id}", response_model=DebugCategoryRead)
async def get_by_id_category(
    category_id: int,
    repo: Annotated["CategoryRepository", Depends(get_category_repository)],
    request: Request,
):
    result = await repo.get_by_id(category_id)
    print(request)
    icon = str(request.base_url) + result.icon["url"]
    return DebugCategoryRead(id=result.id, icon=icon)


@router.get("/", response_model=Page[ReadCategory])
@cache(expire=3600, namespace="category-list")
async def get_all_sql(
    repo: Annotated["CategoryRepository", Depends(get_category_repository)],
    params: Params = Depends(),  # Need for cache in Redis mb FIX
):
    return await apaginate(repo.session, repo.get_select_all())


@router.post(
    "/",
)
async def create_category(
    category_data: Annotated[CreateCategory, Form(media_type="multipart/form-data")],
    repo: Annotated["CategoryRepository", Depends(get_category_repository)],
):
    result = await repo.create(category_data)
    return result
