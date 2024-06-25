# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add the Ngrok token
COPY ngrok_token.txt /app/ngrok_token.txt
RUN ngrok config add-authtoken $(cat /app/ngrok_token.txt)

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
