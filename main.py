# main.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
import joblib
import numpy as np
from pyngrok import ngrok

# Load the trained model
model = joblib.load('iris_model.pkl')

app = FastAPI()

# Define the request model for POST
class IrisRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Define the response model
class IrisResponse(BaseModel):
    prediction: int

@app.get("/")
async def root():
    return {"message": "Hello, this is the Iris prediction API"}

@app.post("/predict", response_model=IrisResponse)
async def predict_post(iris: IrisRequest):
    data = np.array([[iris.sepal_length, iris.sepal_width, iris.petal_length, iris.petal_width]])
    prediction = model.predict(data)[0]
    return IrisResponse(prediction=int(prediction))

@app.get("/predict", response_model=IrisResponse)
async def predict_get(
    sepal_length: float = Query(...),
    sepal_width: float = Query(...),
    petal_length: float = Query(...),
    petal_width: float = Query(...)
):
    data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    prediction = model.predict(data)[0]
    return IrisResponse(prediction=int(prediction))

# Start ngrok tunnel
url = ngrok.connect(8000)
print(f"ngrok tunnel opened at {url}")

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
