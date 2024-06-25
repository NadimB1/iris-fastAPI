# main.py
from fastapi import FastAPI, Depends
from pydantic import BaseModel
import joblib
import numpy as np
from pyngrok import ngrok
import aioredis
import json
import hashlib

# Load the trained model
model = joblib.load('iris_model.pkl')

app = FastAPI()

redis = None

class IrisRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class IrisResponse(BaseModel):
    prediction: int
    source: str

@app.on_event("startup")
async def startup_event():
    global redis
    redis = aioredis.from_url("redis://redis:6379")

@app.on_event("shutdown")
async def shutdown_event():
    await redis.close()

def generate_key(iris: IrisRequest):
    data_string = json.dumps(iris.dict(), sort_keys=True)
    return hashlib.md5(data_string.encode()).hexdigest()

@app.post("/predict", response_model=IrisResponse)
async def predict_post(iris: IrisRequest):
    key = generate_key(iris)
    cached_result = await redis.get(key)

    if cached_result:
        return IrisResponse(prediction=int(cached_result), source="Redis cache")

    data = np.array([[iris.sepal_length, iris.sepal_width, iris.petal_length, iris.petal_width]])
    prediction = model.predict(data)[0]
    await redis.set(key, int(prediction))
    return IrisResponse(prediction=int(prediction), source="model.predict")

@app.get("/predict", response_model=IrisResponse)
async def predict_get(
    sepal_length: float,
    sepal_width: float,
    petal_length: float,
    petal_width: float
):
    iris = IrisRequest(sepal_length=sepal_length, sepal_width=sepal_width, petal_length=petal_length, petal_width=petal_width)
    key = generate_key(iris)
    cached_result = await redis.get(key)

    if cached_result:
        return IrisResponse(prediction=int(cached_result), source="Redis cache")

    data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    prediction = model.predict(data)[0]
    await redis.set(key, int(prediction))
    return IrisResponse(prediction=int(prediction), source="model.predict")

# Start ngrok tunnel
url = ngrok.connect(8000)
print(f"ngrok tunnel opened at {url}")

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
