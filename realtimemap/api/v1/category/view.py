from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import apaginate

from crud.category.repository import CategoryRepository
from dependencies.crud import get_category_repository
from models.category.schemas import ReadCategory

router = APIRouter(prefix="/category", tags=["category"])

# Получение всех категорий
#
# Создание для пользователей, Неизвестно, вероятно нельзя
#
#
#


# @router.get("/", response_model=Page[ReadCategory])
# async def get_category(
#     repo: Annotated["CategoryRepository", Depends(get_category_repository)],
# ):
#     result = await repo.get_all()
#     return paginate(result)


@router.get("/sql", response_model=Page[ReadCategory])
async def get_all_sql(
    repo: Annotated["CategoryRepository", Depends(get_category_repository)],
):
    return await apaginate(repo.session, repo.get_select_all())
