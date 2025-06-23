from fastapi import FastAPI
from auth import router as auth_router
from chat import router as chat_router
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from chat import router as chat_router


app = FastAPI()

# MongoDB connection
client = AsyncIOMotorClient("mongodb+srv://rajuvenkat0007:<db_password>@chatdb.5hg5xf1.mongodb.net/?retryWrites=true&w=majority&appName=chatdb")
db = client["chatdb"]

# Pass DB to routes
app.state.db = db
app.include_router(auth_router, prefix="/auth")
app.include_router(chat_router, prefix="/chat")

@app.get("/")
def root():
    return {"message": "Chat App Backend Running"}
