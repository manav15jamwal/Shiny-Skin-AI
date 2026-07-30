from fastapi import APIRouter,Depends,File,UploadFile,HTTPException
from prediction_model import analyse
from auth import USER_DEPENDENCY,DB
import auth_services,models


router = APIRouter(
    tags=["Prediction"],
    prefix="/prediction"
)


@router.get("/fetch_all")
async def fetch(user:USER_DEPENDENCY,db:DB):
    current_user = auth_services.current_user(user)
    if current_user:
       return db.query(models.Prediction).filter(models.Prediction.user_id==current_user.get("id")).all()

@router.post("/predict")
async def predict(user:USER_DEPENDENCY,db:DB,file:UploadFile=File(...)):
    
    current_user = auth_services.current_user(user)
    image_bytes = await file.read()
    if current_user:
       acne_response,confidence_response = analyse(image_bytes)
       prediction = models.Prediction(
           user_id = current_user.get("id"),
           acne = acne_response,
           confidence = confidence_response
       )
       db.add(prediction)
       db.commit()
       return prediction
    raise HTTPException(status_code=401)
