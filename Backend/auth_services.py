import auth_schemas,models,security_utils
from sqlalchemy.orm import Session
from product_schemas import Product


#Fetching all info of Users/User
def users(db:Session,user_id = None):
    if not user_id:
        user = db.query(models.User).all()
    else:
        user = db.query(models.User).filter(models.User.id==user_id).first()
    return user

def create_user(user:auth_schemas.Create_User,db:Session):
    new_user = models.User(
        user_name = user.name,
        hashed_password = security_utils.hash(user.password),
        email = user.email
    )
    if db.query(models.User).filter(models.User.email==user.email).first():
        return False
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
#Token Generation
def token(email:str,user_id:int):
    token = security_utils.create_token(email,user_id)
    return {
        "access_token":token,
        "type":"bearer"
    }

#Authentication
def authenticate(email:str,password:str,db:Session):
    user = db.query(models.User).filter(models.User.email==email).first()
    if user:
        verify = security_utils.verify(password,user.hashed_password)
    
        if verify:
            return user
        return verify
    return user

#Updating existing user details
def update(db:Session,user_id:int,user:auth_schemas.Update_User):
    current_user = db.query(models.User).filter(models.User.id==user_id).first()
    if user.password:
        hash = security_utils.hash(user.password)
        user.password = hash
    
    if current_user:
        current_user.hashed_password = user.password
        update = user.model_dump(exclude_unset = True)

        for key,value in update.items():
            setattr(current_user,key,value)
            
        db.commit()
        db.refresh(current_user)
        return True
    return False

#Current User
def current_user(user:str):
    return security_utils.current_user(user)

#Delete User based on {user_id}

def delete(db:Session,user_id : int):
    user = db.query(models.User).filter(models.User==user_id).first()
    db.delete(user)
    db.commit()

#Creating a new Product
def create_product(product:Product,db:Session):
    new_product = models.Products(**product.model_dump())
    db.add(new_product)
    db.commit()

#Fetching all products
def fetch_all_products(db:Session,type=None):
    if type==None:
        products = db.query(models.Products).all()
    else:
        products = db.query(models.Products).filter(models.Products.type==type).all()
    if products:
        products = [  {
            "id" : product.id,
            "name" : product.name,
            "category" : product.category,
            "type" : product.type,
            "usage_time" :product. usage_time,
            "description" : product. description,
            "price":product.price,
            "image_url" : product.image_url
        } for product in products]
        return products
    return "No products found"

#Products by id
def fetch_products_by_ids(db:Session,products):
    product_list = [db.query(models.Products).filter(models.Products.id == product_id).first() for product_id in products]
    if product_list:
        products = [  {
            "id" : product.id,
            "name" : product.name,
            "category" : product.category,
            "type" : product.type,
            "usage_time" :product. usage_time,
            "description" : product. description,
             "price":product.price,
            "image_url" : product.image_url
        } for product in product_list]
        return products
    return []