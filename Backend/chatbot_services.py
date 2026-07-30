from openai import OpenAI
from dotenv import load_dotenv
import auth_schemas,models,security_utils
from security_utils import format_products
from sqlalchemy.orm import Session
load_dotenv()
import os

client = OpenAI(api_key = os.getenv("API_KEY"))

def askllm(message:str):
   try:
       response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message
        )
       return response.choices[0].message.content
   except Exception as e:
       print("openai error:",e)
       raise e
   

def chat_history(user_id:int,db:Session):
    chat_history = db.query(models.ChatHistory).filter(models.ChatHistory.user_id==user_id).order_by(models.ChatHistory.id.desc())\
    .limit(5).all()
    return chat_history

def build_messages(user, prediction, products, chats, user_message):

    messages = []

    messages.append({
    "role": "system",
    "content": f"""
You are Shiny, a professional skincare advisor for Glow SKINN.

User name: {user.user_name}
Skin condition: {prediction.acne}

Available products:
{products}

Your job:
- Recommend ONLY products from the list above
- Build a proper skincare routine.
- If user enquires about one or more products explain it like a skincare specialist do not share info such as "type" like a pre registered format . Keep approach as a human.
- Explain briefly why each product is used
- Donot expose product ids to the user at all
- Keep response natural and friendly
- Do NOT suggest external products
- Your name is shiny agent working for skincare company Glow SKINN designed by AIML student Manav Jamwal.
- if message is "Took a test" guide user about condition of his skin and  for best skincare routine.

IMPORTANT:

You MUST respond ONLY in valid JSON format:

{{
  "message": "your explanation",
  "product_ids": [1, 2, 3]
}}

Rules:

- Do not reply in aetriks(**).No need to bold/italic any product.
- While listing products in "message" use double "\n" for separating products.
- Only include product IDs from the list
- Do NOT return anything outside JSON
- Do NOT include extra text before or after JSON
- If user prompts some filtering or requirements or specific product do update the "product_ids" accordingly 
- Do not send duplicates in "product_ids"
"""
})

    for chat in reversed(chats):
        messages.append({
        "role": "user",
        "content": chat.message
            })
        messages.append({
            "role": "assistant",
            "content": chat.response
            })

    # 🔹 Current user input
    messages.append({
        "role": "user",
        "content": user_message
    })

    return messages
def save_history(user_id:int,msg:str,reply:str,db:Session):
    history = models.ChatHistory(
    user_id = user_id,
    message = msg,
    response = reply
    )
    db.add(history)
    db.commit()