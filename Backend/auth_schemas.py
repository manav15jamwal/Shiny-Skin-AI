from pydantic import BaseModel

class Create_User(BaseModel):
    name : str
    password:str
    email:str

class Update_User(BaseModel):
    name : str | None = None
    password:str | None = None
    email:str | None = None
class token(BaseModel):
    email:str
    user_id : int
class token_raw(BaseModel):
    token:str
