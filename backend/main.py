from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.assistant import CreditCardAssistant

bot = CreditCardAssistant()

app = FastAPI()

# Allow React fpirontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    message: str

@app.post("/chat")
def chat(query: Query):
    response = bot.handle(query.message)
    return {"reply": response}
