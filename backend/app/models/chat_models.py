from pydantic import BaseModel, constr

class ChatRequest(BaseModel):
    message: constr(min_length=1, max_length=500)

class ChatResponse(BaseModel):
    response: str
