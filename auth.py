from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()
SECRET_KEY = "supersecretkey"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MONGO_URI = "mongodb+srv://<your-mongo-user>:<your-pass>@cluster0.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGO_URI)
db = client["chatdb"]

class User(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(user: User):
    existing = await db.users.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_pwd = pwd_context.hash(user.password)
    await db.users.insert_one({"username": user.username, "password": hashed_pwd})
    return {"message": "User registered"}

@router.post("/login")
async def login(user: User):
    record = await db.users.find_one({"username": user.username})
    if not record or not pwd_context.verify(user.password, record["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"username": user.username}, SECRET_KEY)
    return {"token": token}
