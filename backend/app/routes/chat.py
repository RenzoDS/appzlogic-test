from fastapi import APIRouter
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.huggingface_service import send_message

router = APIRouter()

@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with the AI",
    description="""
    Sends a message to the AI chatbot and returns its response.
    
    **Request Body:**
    - **message**: A string between 1 and 500 characters.

    **Responses:**
    - **200 OK**: Successfully processed message.
    - **422 Unprocessable Entity**: Validation error on input.
    - **500 Internal Server Error**: Error while processing the request or an external API error.
    """,
    responses={
        200: {"description": "Successful Response", "content": {"application/json": {"example": {"response": "Hello, test response!"}}}},
        422: {"description": "Validation Error", "content": {"application/json": {"example": {"detail": [{"loc": ["body", "message"], "msg": "field required", "type": "value_error.missing"}]}}}},
        500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"error": "An error occurred", "message": "Error calling Hugging Face API: ...", "path": "/api/chat"}}}},
    }
)
async def chat_endpoint(chat_request: ChatRequest):
    user_input = chat_request.message.strip()
    chatbot_response = await send_message(user_input)
    return ChatResponse(response=chatbot_response)
