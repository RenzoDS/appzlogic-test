from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat

app = FastAPI(
    title="Chat API",
    description="This API allows you to chat with an AI powered by Hugging Face's Blenderbot model. It includes endpoints for sending messages and handling errors gracefully.",
    version="1.0.0",
    contact={
        "name": "Renzo DS",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTPException handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "An error occurred",
            "message": exc.detail,
            "path": str(request.url),
        },
    )


app.include_router(chat.router, prefix="/api")