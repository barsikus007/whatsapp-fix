from src.models.click import ClickBase


class IClickCreate(ClickBase):
    pass


class IClickRead(ClickBase):
    id: int


class IClickUpdate(IClickCreate):
    pass
