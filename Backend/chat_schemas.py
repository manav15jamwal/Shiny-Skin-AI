from pydantic import BaseModel

class Chat(BaseModel):
    msg:str

class Item(BaseModel):
    product_id :int