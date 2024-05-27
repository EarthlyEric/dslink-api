from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app import database

urls = APIRouter()

@urls.get("/{hash}")
async def redirect_to(hash:str):
    url_entry = await database.urls.find_one({"hash": hash})
    if url_entry:
        return {"url": url_entry["url"]}
    
    raise HTTPException(status_code=404, detail="Short URL not found")

@urls.get("/")
async def index():
    return {"message":"Hello World"}
