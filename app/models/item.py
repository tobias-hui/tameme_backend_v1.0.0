from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str
    price: float

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemInDB(ItemBase):
    id: int

    class Config:
        orm_mode = True
