from typing import Optional, Annotated, List

from fastapi import APIRouter, Depends, Form
from pydantic import BaseModel, Field
from starlette.requests import Request

from api.v1.auth.fastapi_users import current_active_user
from crud.mark import MarkRepository
from dependencies.crud import get_mark_repository
from models import TypeMark, User
from schemas.mark import CreateMarkRequest, ReadMark

router = APIRouter(prefix="/marks", tags=["Marks"])


class MarkParams(BaseModel):
    latitude: float = Field(..., ge=-180, le=180, examples=["75.445675"])
    longitude: float = Field(..., ge=-90, le=90, examples=["63.201907"])
    radius: int = Field(500, description="Search radius in meters.")
    srid: int = Field(4326, description="SRID")
    type_mark: Optional[TypeMark] = None


@router.get("/", response_model=List[ReadMark])
async def get_marks(
    repo: Annotated["MarkRepository", Depends(get_mark_repository)],
    params: MarkParams = Depends(),
):
    result = await repo.get_marks(**params.model_dump())
    return result


@router.post("/", response_model=ReadMark)
async def create_mark_point(
    mark: Annotated[CreateMarkRequest, Form(media_type="multipart/form-data")],
    user: Annotated["User", Depends(current_active_user)],
    repo: Annotated["MarkRepository", Depends(get_mark_repository)],
):
    """
    Protected endpoint for create mark.
    """
    instance = await repo.create_mark(mark, user)
    data = instance.__dict__
    data.pop("geom")  # FIX THIS
    return data


@router.get("/list/", response_model=List[ReadMark])
async def get_mark_list(
    repo: Annotated["MarkRepository", Depends(get_mark_repository)],
):
    result = await repo.get_all_marks()
    return result


@router.get(
    "/{mark_id}/",
)
async def get_mark(
    mark_id: int,
    repo: Annotated["MarkRepository", Depends(get_mark_repository)],
    request: Request,
):
    result = await repo.get_mark_by_id(mark_id)
    result = result.__dict__
    result.pop("geom")
    return ReadMark.model_validate(result, context={"request": request})


@router.delete("/{mark_id}")
async def delete_mark(
    mark_id: int,
    user: Annotated["User", Depends(current_active_user)],
):
    pass
