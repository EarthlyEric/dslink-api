from datetime import datetime, timezone ,timedelta
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from core.utils import utils
from core.models import generateSchema, lookupSchema
from core.config import Config
from app import database, redisClient

api = APIRouter()

config = Config()

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
    await redisClient.set(hash, str(request.url),ex=60*60*24*request.expiryDays)
    if databaseResult.inserted_id:
        await database.system.update_one({"type":"statistic"},{"$inc":{"route./generate.sucess":1}})
        return {"hash": hash,"expiryDays": request.expiryDays}
    
    await database.system.update_one({"type":"statistic"},{"$inc":{"route./generate.fail":1}})
    raise HTTPException(status_code=500, detail="Failed to shorten URL")

@api.get("/health")
async def health():
    await database.system.update_one({"type":"statistic"},{"$inc":{"route./health":1}})
    return {"status":"ok"}

@api.get("/info")
async def version():
    await database.system.update_one({"type":"statistic"},{"$inc":{"route./info":1}})
    return {"name":"DSLink",
            "version":"1.0.0",
            "buildid":config.buildid }

@api.get("/statistic")
async def statistic():
    await database.system.update_one({"type":"statistic"},{"$inc":{"route./statistic":1}})
    databaseSystemResult = await database.system.find_one({"type":"statistic"})
    links=await database.links.count_documents()
    return await database.system.insert_one({
            "type":"statistic",
            "route":{
                "api":{
                    "/generate":{
                        "sucess":databaseSystemResult["route"]["api"]["/generate"]["sucess"],
                        "fail":databaseSystemResult["route"]["api"]["/generate"]["fail"]
                        },
                    "/lookup":{
                        "sucess":databaseSystemResult["route"]["api"]["/lookup"]["sucess"],
                        "fail":databaseSystemResult["route"]["api"]["/lookup"]["fail"]
                    },
                    "/health":databaseSystemResult["route"]["api"]["/health"],
                    "/info":databaseSystemResult["route"]["api"]["/info"],
                    "/statistic":databaseSystemResult["route"]["api"]["/statistic"]
                    },
                "web":{
                    "redirect":{
                        "sucess":databaseSystemResult["route"]["web"]["redirect"]["sucess"],
                        "fail":databaseSystemResult["route"]["web"]["redirect"]["fail"]
                    }
                },
                "links":{"totals":links}
            }
            })

@api.post("/lookup")
async def lookup(request:lookupSchema):
    hash = request.hash
    url = await redisClient.get(hash).decode('utf-8')
    if url is None:
        url_entry = await database.links.find_one({"hash": hash})
        if url_entry:
            await redisClient.set(hash, str(url_entry["url"]))
            await database.system.update_one({"type":"statistic"},{"$inc":{"route./lookup.sucess":1}})
            return {"url": url_entry["url"]}
    else:
        await database.system.update_one({"type":"statistic"},{"$inc":{"route./lookup.sucess":1}})
        return {"url": url}
    
    await database.system.update_one({"type":"statistic"},{"$inc":{"route./lookup.fail":1}})
    raise HTTPException(status_code=404, detail="Short URL not found")




