from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from core.utils import utils
from core.models import generateSchema
from app import database, redisClient

api = APIRouter()

@api.post("/generate")
async def generate(request:generateSchema):
    hash = utils.generateHash()
    while await database.links.find_one({"hash":hash}):
        hash = utils.generateHash()

    databaseResult = await database.urls.insert_one({"url": str(request.url), "hash": hash})
    redisResult = await redisClient.set(hash, str(request.url))
    if databaseResult.inserted_id:
        return {"hash": hash}
    
    raise HTTPException(status_code=500, detail="Failed to shorten URL")

