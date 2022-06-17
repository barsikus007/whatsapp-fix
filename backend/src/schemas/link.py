from src.models.link import LinkBase


class ILinkCreate(LinkBase):
    pass


class ILinkRead(LinkBase):
    id: int


class ILinkUpdate(ILinkCreate):
    pass
