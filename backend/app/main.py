
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, constr
import requests
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Pydantic models
class ChatRequest(BaseModel):
    message: constr(min_length=1, max_length=500)

class ChatResponse(BaseModel):
    response: str

# Hugging Face Inference API configuration to move to environment variables
HF_API_TOKEN = "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"
HF_MODEL_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    user_input = chat_request.message.strip()
    payload = {"inputs": user_input}

    try:
        response = requests.post(HF_MODEL_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except Exception as e:
        logger.error(f"Error during request to external API: {e}")
        raise HTTPException(status_code=500, detail="Error calling chat API")

    try:
        data = response.json()
    except Exception as e:
        logger.error(f"Error parsing JSON response: {e}")
        raise HTTPException(status_code=500, detail="Invalid response format from chat API")

    if isinstance(data, dict) and data.get("error"):
        error_msg = data.get("error", "Unknown error")
        logger.error(f"External API error: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

    try:
        chatbot_response = data[0].get("generated_text", "")
    except Exception as e:
        logger.error(f"Error extracting chatbot response: {e}")
        raise HTTPException(status_code=500, detail="Error processing chat response")

    logger.info(f"Successfully processed message: {user_input}")
    return ChatResponse(response=chatbot_response)
