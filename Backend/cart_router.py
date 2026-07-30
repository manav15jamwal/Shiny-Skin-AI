from fastapi import APIRouter
from auth import USER_DEPENDENCY, DB
import auth_services, models, chat_schemas

router = APIRouter(
    tags=["Cart"],
    prefix="/cart"
)


@router.post("/add")
def add_to_cart(data: chat_schemas.Item, user: USER_DEPENDENCY, db: DB):

    current_user = auth_services.current_user(user)
    user_id = current_user.get("id")

    existing = db.query(models.Cart).filter(
        models.Cart.user_id == user_id,
        models.Cart.product_id == data.product_id
    ).first()

    if existing:
        existing.quantity += 1
    else:
        new_item = models.Cart(
            user_id=user_id,
            product_id=data.product_id,
            quantity=1
        )
        db.add(new_item)

    db.commit()

    return {"message": "Added to cart"}



@router.get("/my-cart")
def get_cart(user: USER_DEPENDENCY, db: DB):

    current_user = auth_services.current_user(user)
    user_id = current_user.get("id")

    cart_items = db.query(models.Cart).filter(
        models.Cart.user_id == user_id
    ).all()

    result = []

    for item in cart_items:
       
        product = db.query(models.Products).filter(
            models.Products.id == item.product_id
        ).first()

        if product:
            result.append({
                "product_id": product.id,
                "name": product.name,
                "category": product.category,
                "usage_time": product.usage_time,
                "description": product.description,
                "quantity": item.quantity,
                "price":product.price,
                "image_url":product.image_url
            })

    return result



@router.delete("/remove/{product_id}")
def remove_from_cart(product_id:int, user: USER_DEPENDENCY, db: DB):

    current_user = auth_services.current_user(user)
    user_id = current_user.get("id")

    existing = db.query(models.Cart).filter(
        models.Cart.user_id == user_id,
        models.Cart.product_id == product_id
    ).first()
    if existing.quantity <= 1:
        db.delete(existing)

    else:
        existing.quantity -= 1

    db.commit()

    return {"message": "Removed from cart"}
#Removes entire item despite the quanity
@router.delete("/remove_all/{product_id}")
def remove_from_cart(product_id: int, user: USER_DEPENDENCY, db: DB):

    current_user = auth_services.current_user(user)
    user_id = current_user.get("id")

    item = db.query(models.Cart).filter(
        models.Cart.user_id == user_id,
        models.Cart.product_id == product_id
    ).first()

    if item:
        db.delete(item)
        db.commit()

    return {"message": "Removed from cart"}

#Empties whole cart.
@router.delete("/empty_cart")
async def empty_cart(user:USER_DEPENDENCY,db:DB):
    
    current_user = auth_services.current_user(user)
    user_id = current_user.get("id")

    db.query(models.Cart).filter(
        models.Cart.user_id == user_id
    ).delete()
    db.commit()
    return {"message":"Cart-emptied"}

    