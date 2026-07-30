from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import auth,prediction,chatbot_router,cart_router
from database import Base,engine
Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]

    
)
app.include_router(auth.router)
app.include_router(prediction.router)
app.include_router(chatbot_router.router)
app.include_router(cart_router.router)

