from typing import List, Union
from pydantic import BaseModel


class ItemBase(BaseModel):
    project_id: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    issue_id: str
    issue_type: str
    package: str

    class Config:
        orm_mode = True
