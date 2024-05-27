from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from app import database,redisClient

urls = APIRouter()

@urls.get("/{hash}")
async def redirect_to(hash:str):
    url = await redisClient.get(hash)
    if url is None:
        url_entry = await database.urls.find_one({"hash": hash})
        if url_entry:
            return {"url": url_entry["url"]}
    else:
        return {"url": url}
    
    raise HTTPException(status_code=404, detail="Short URL not found")

@urls.get("/")
async def index():
    return {"message":"Hello World"}
