from uuid import UUID
from sqlmodel import Field, SQLModel

from src.models.base import Base


class ClickBase(SQLModel):
    ip: str = Field(
        nullable=False, index=True
    )
    number: str


class Click(ClickBase, Base, table=True):
    pass
