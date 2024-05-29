from datetime import datetime, timezone ,timedelta
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from core.utils import utils
from core.models import generateSchema, lookupSchema
from app import database, redisClient

api = APIRouter()

@api.post("/generate")
async def generate(request:generateSchema):
    
    hash = utils.generateHash()
    while await database.links.find_one({"hash":hash}):
        hash = utils.generateHash()

    expiryDays = datetime.now(timezone.utc) + timedelta(days=request.expiryDays)

    databaseResult = await database.links.insert_one({
        "url": str(request.url), 
        "hash": hash,
        "expirydays": expiryDays,
    })
    redisResult = await redisClient.set(hash, str(request.url),ex=60*60*24*request.expiryDays)
    if databaseResult.inserted_id:
        return {"hash": hash,"expiryDays": request.expiryDays}
    
    raise HTTPException(status_code=500, detail="Failed to shorten URL")

@api.post("/lookup")
async def lookup(request:lookupSchema):
    hash = request.hash
    url = await redisClient.get(hash).decode('utf-8')
    if url is None:
        url_entry = await database.links.find_one({"hash": hash})
        if url_entry:
            redisResult = await redisClient.set(hash, str(url_entry["url"]))
            return {"url": url_entry["url"]}
    else:
        return {"url": url}
    
    raise HTTPException(status_code=404, detail="Short URL not found")



