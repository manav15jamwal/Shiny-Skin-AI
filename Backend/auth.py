from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import auth_services,auth_schemas
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from product_schemas import Product
from security_utils import current_user
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

DB = Annotated[Session,Depends(get_db)]
USER_DEPENDENCY = Annotated[str,Depends(oauth_scheme)]
router = APIRouter(
    prefix="/auth",
    tags = ["Auth"]
)
@router.get("/users")
async def check(db:DB,user:USER_DEPENDENCY):
    current_user = auth_services.current_user(user)
    if current_user.get("id")==1:
        return auth_services.users(db)
    raise HTTPException(status_code=401,detail="Not Authenticated")
@router.get("/token_check")
async def check_token(token:auth_schemas.token_raw):
    return current_user(token)
    

@router.get("/user")
async def check(db:DB,user:USER_DEPENDENCY):
    current_user = auth_services.current_user(user)
    if current_user:
        return auth_services.users(db,current_user.get("id"))
    raise HTTPException(status_code=404,detail="User Not Found")

@router.post("/register")
async def register(user:auth_schemas.Create_User,db:DB):
    if auth_services.create_user(user,db):
        return{
            "message":"Registered successfully."
        }
    raise HTTPException(status_code=401)

@router.post("/token")
async def login(user:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    authentication = auth_services.authenticate(user.username,user.password,db)
    if authentication:
        token = auth_services.token(authentication.email,authentication.id)
        print(token)
        return token
    return {
        "message":"Not Authenticated.Please check your credentials"
    }

@router.put("/update")
async def update(db:DB,update_user:auth_schemas.Update_User,user:USER_DEPENDENCY):
    current_user = auth_services.current_user(user)
    if current_user:
        user_id = current_user.get("id")
        return auth_services.update(db,user_id,update_user)
    raise HTTPException(status_code=401,detail="Not Authenticated")

@router.delete("/delete")
async def delete(user:USER_DEPENDENCY,db:DB):
    current_user = auth_services.current_user(user)
    if current_user:
        user_id = current_user.get("id")
        return auth_services.delete(db,user_id)
    raise HTTPException(status_code=401,detail="Not Authenticated")

@router.get("/fetch_products")
async def fetchall(db:DB):
    return auth_services.fetch_all_products(db)
@router.get("/fetch_products/{type}")
async def fetchall(db:DB,type:str):
    return auth_services.fetch_all_products(db,type)
@router.post("/new_product")
async def create_product(product:Product,db:DB):
    return auth_services.create_product(product,db)


