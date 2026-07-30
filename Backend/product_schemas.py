from pydantic import BaseModel
from models import Products

class Product(BaseModel):
    name : str
    category :str
    type : str
    usage_time :str
    description :str
    price:float
    image_url:str
