from fastapi import APIRouter,Depends,HTTPException
from auth import USER_DEPENDENCY,DB
import auth_services,models
import chatbot_services
import json
from chat_schemas import Chat

router =  APIRouter(
    tags = ["Chatbot"],
    prefix="/chatbot"
)
@router.get("/history")
def get_history(user: USER_DEPENDENCY, db: DB):
    current_user = auth_services.current_user(user)
    user_id = current_user.get("id")
    client = db.query(models.User).filter(models.User.id==user_id).first()

    chats = db.query(models.ChatHistory)\
        .filter(models.ChatHistory.user_id == user_id)\
        .order_by(models.ChatHistory.id.desc()).limit(8)\
        .all()

    history = [
        {
            "message": chat.message,
            "response": chat.response
        }
        for chat in chats
    ]
    return {
    "name": client.user_name,
    "history": history
}
@router.post("/chat")
async def chat(msg:Chat,user:USER_DEPENDENCY,db:DB):
    msg = msg.msg
    current_user = auth_services.current_user(user)
    if current_user:
        
        user_id = current_user.get("id")
        user= db.query(models.User).filter(models.User.id==user_id).first()
        prediction = db.query(models.Prediction).\
        filter(models.Prediction.user_id==user_id).order_by(models.Prediction.id.desc()).first()
        chat = chatbot_services.chat_history(user_id,db)
        products = auth_services.fetch_all_products(db,prediction.acne)
        products = products
        message = chatbot_services.build_messages(user,prediction,products,chat,msg)
        response = chatbot_services.askllm(message)
       
        parsed = json.loads(response)
        message = parsed.get("message")
        product_ids = parsed.get("product_ids",[])
        products = auth_services.fetch_products_by_ids(db,product_ids)
        chatbot_services.save_history(user_id,msg,response,db)
        print( {"message":message,
                "products":products})
        return {"message":message,
                "products":products}

        
    raise HTTPException(status_code=401,detail="Not Authenticated")

