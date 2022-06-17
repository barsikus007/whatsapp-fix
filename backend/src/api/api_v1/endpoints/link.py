import re
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, Params
from sqlmodel.ext.asyncio.session import AsyncSession

from src import crud
from src.api import deps
from src.models.user import User
from src.schemas.link import ILinkCreate, ILinkRead, ILinkUpdate
from src.schemas.common import (
    IGetResponseBase,
    IPostResponseBase,
    IPutResponseBase,
    IDeleteResponseBase,
)


router = APIRouter()


@router.get("/", response_model=IGetResponseBase[Page[ILinkRead]])
async def read_links_list(
    *,
    params: Params = Depends(),
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    links = await crud.link.get_multi(db, params=params)
    return IGetResponseBase[Page[ILinkRead]](data=links)


@router.post("/", response_model=IPostResponseBase[ILinkRead])
async def create_link(
    *,
    new_link: ILinkCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
):
    if not re.match(r"(\+\d{7,11},?)+", new_link.numbers):
        raise HTTPException(
            status_code=400,
            detail="numbers must have format '+79111111111,+79222222222,+79333333333,+79444444444,+79555555555'")
    link = await crud.link.get_by_name(db, name=new_link.name)
    if link:
        raise HTTPException(status_code=400, detail="There is already a link with same name")
    link = await crud.link.create(db, obj_in=new_link)
    return IPostResponseBase[ILinkRead](data=link)


@router.delete("/{link_id}", response_model=IDeleteResponseBase[ILinkRead])
async def remove_link(
    *,
    link_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
):
    link = await crud.link.get(db, id_=link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    link = await crud.link.remove(db, id_=link_id)
    return IDeleteResponseBase[ILinkRead](
        data=link
    )


@router.get("/{link_id}", response_model=IGetResponseBase[ILinkRead])
async def get_link_by_id(
    *,
    link_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
):
    link = await crud.link.get(db, id_=link_id)
    return IGetResponseBase[ILinkRead](data=link)


@router.put("/{link_id}", response_model=IPutResponseBase[ILinkRead])
async def update_link(
    *,
    db: AsyncSession = Depends(deps.get_db),
    link_id: int,
    link_in: ILinkUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
):
    link = await crud.link.get(db, id_=link_id)
    if not link:
        raise HTTPException(
            status_code=404,
            detail="The link with this id does not exist in the system",
        )
    if link_db := await crud.link.get_by_name(db, name=link_in.name):
        if link.id != link_db.id:
            raise HTTPException(status_code=400, detail="There is already a link with same name")
    link = await crud.link.update(db, obj_db=link, obj_in=link_in)
    return IPutResponseBase[ILinkRead](data=link)
