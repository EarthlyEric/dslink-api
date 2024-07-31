from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from app import database , redisClient

urls = APIRouter()

@urls.get("/{hash}")
async def redirect_to(hash:str):
    url = await redisClient.get(hash)
    url = url.decode('utf-8') if url else None
    if url is None:
        url_entry = await database.links.find_one({"hash": hash})
        if url_entry:
            await redisClient.set(hash, str(url_entry["url"]))
            await database.system.update_one({"type":"statistic"},{"$inc":{"route.web.redirect.sucess":1}})
            return RedirectResponse(url=url_entry["url"],status_code=301)
    else:
        await database.system.update_one({"type":"statistic"},{"$inc":{"route.web.redirect.sucess":1}})
        return RedirectResponse(url=url,status_code=301)
    
    await database.system.update_one({"type":"statistic"},{"$inc":{"route.web.redirect.fail":1}})
    raise HTTPException(status_code=404, detail="Short URL not found")

@urls.get("/")
async def index():
    return {"message":"Hello World"}
