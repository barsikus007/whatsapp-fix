from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.link import Link
from src.schemas.link import ILinkCreate, ILinkUpdate

from .base import CRUDBase


class CRUDLink(CRUDBase[Link, ILinkCreate, ILinkUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Link | None:
        users = await db.exec(select(Link).where(Link.name == name))  # type: ignore
        return users.first()


link = CRUDLink(Link)
