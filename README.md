# Iris Prediction FastAPI Application

This is a FastAPI application that predicts the species of an Iris flower based on its sepal length, sepal width, petal length, and petal width. The application uses a pre-trained machine learning model and caches the predictions using Redis. The application is also accessible via Ngrok.

## Prerequisites

- Docker
- Docker Compose
- Ngrok account (for Ngrok authtoken) : https://dashboard.ngrok.com/get-started/your-authtoken

## Setup

1. **Clone the repository**:

   ```sh
   git clone <repository_url>
   cd iris-fastapi

2. **Add your Ngrok authtoken**:

Create a file named ngrok_token.txt in the root directory of the project and add your Ngrok authtoken to this file.

    <Your_Ngrok_Token>

3. **Install dependencies**:

Ensure you have Docker and Docker Compose installed on your machine. Then, run the following commands to build and start the services:

    docker-compose up --build

## Testing the Application

Access the application:

Once the services are up and running, the application will be accessible at
    http://localhost:8000/predict?sepal_length=5.1&sepal_width=3.5&petal_length=1.4&petal_width=0.2

Make a POST request for predictions:

Use curl, Postman, or any HTTP client to make a POST request to the /predict endpoint with the required parameters in the JSON body.

Using curl:
curl -X POST "http://localhost:8000/predict" -H "Content-Type: 

     application/json" -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
    }'

## Checking if the prediction is cashed

    docker run -it --network=iris-fastapi_default --rm redis redis-cli -h redis

Then show the keys

    KEYS *

and finally copy that key and execute : 

    GET <your_cache_key>
