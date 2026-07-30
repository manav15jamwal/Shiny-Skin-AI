from keras.models import load_model
from PIL import Image
import io, numpy as np

#Loading model
model = load_model("acne_detection.keras")

#Preprocessing Image
def preprocess(img):
    image = Image.open(io.BytesIO(img))
    image = image.convert("RGB")
    image = image.resize((64,64))
    image_array  = np.array(image)
    image_array = np.expand_dims((image_array/255.0),axis=0)
    return image_array

def analyse(img):
    image = preprocess(img)
    pred = model.predict(image)[0][0]

    label = "no acne" if pred > 0.5 else "acne"
    confidence = round(float(pred),2)
    return(label,confidence)