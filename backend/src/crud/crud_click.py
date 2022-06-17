from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.click import Click
from src.schemas.click import IClickCreate, IClickUpdate

from .base import CRUDBase


class CRUDClick(CRUDBase[Click, IClickCreate, IClickUpdate]):
    async def get_by_ip(self, db: AsyncSession, *, ip: str) -> Click | None:
        users = await db.exec(select(Click).where(Click.ip == ip))  # type: ignore
        return users.first()


click = CRUDClick(Click)