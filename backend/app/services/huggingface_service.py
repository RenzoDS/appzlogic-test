import os
import httpx
from fastapi import HTTPException

#Temporary API Token and Model URL, need to move to environment variables
HF_API_TOKEN = "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"
HF_MODEL_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}

async def send_message(message: str) -> str:
    payload = {"inputs": message}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(HF_MODEL_URL, headers=headers, json=payload)
            response.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calling Hugging Face API: {str(e)}")

    data = response.json()
    if isinstance(data, dict) and data.get("error"):
        raise HTTPException(status_code=500, detail=data["error"])

    # Extract the chatbot response
    chatbot_response = data[0].get("generated_text", "")
    return chatbot_response