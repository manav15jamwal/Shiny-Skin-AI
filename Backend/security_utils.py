from jose import JWTError,jwt
from passlib.context import CryptContext
from datetime import datetime , timedelta,timezone
from dotenv import load_dotenv
import os
load_dotenv()
context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

SECURITY_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGO")

def hash(password:str):
    return context.hash(password)
def verify(password,hash:str):
    return context.verify(password,hash)

def create_token(email:str,user_id:int):
    to_encode = {
        "sub":email,
        "id":user_id
    }
    expiry = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp":expiry})
    token =  jwt.encode(to_encode,SECURITY_KEY,algorithm=ALGORITHM)
    return token

def current_user(user:str):
    print(user)
    try:
        payload = jwt.decode(user,SECURITY_KEY,algorithms=[ALGORITHM])
        if payload:
            return payload
        return False
    except JWTError as e:
        print(e)
        return None
def format_products(products):
    return [
        {
            "name": p.name,
            "type": p.type,
            "usage": p.usage_time,
            "description": p.description
        }
        for p in products
    ]