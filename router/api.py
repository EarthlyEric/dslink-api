from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from core.utils import utils
from core.models import generateSchema
from app import database

api = APIRouter()

@api.post("/generate")
async def generate(request:generateSchema):
    hash = utils.generateHash()
    while await database.links.find_one({"hash":hash}):
        hash = utils.generateHash()

    result = await database.urls.insert_one({"url": str(request.url), "hash": hash})
    if result.inserted_id:
        return {"hash": hash}
    
    raise HTTPException(status_code=500, detail="Failed to shorten URL")

