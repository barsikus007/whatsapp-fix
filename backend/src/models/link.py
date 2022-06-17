from enum import Enum
from sqlmodel import Field, SQLModel

from src.models.base import Base


class LinkType(str, Enum):
    ip = 'ip'
    cookie = 'cookie'


class LinkBase(SQLModel):
    name: str
    numbers: str
    type: LinkType


class Link(LinkBase, Base, table=True):
    pass
