from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass 


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        owm_mode = True

    
class UserBase(BaseModel):
    email: str 


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    item = list[Item] = []

    class Conf:
        orm_mode = True