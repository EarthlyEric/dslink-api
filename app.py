import pymongo
import dns.resolver
import redis.asyncio as redis
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from core.config import Config
from motor.motor_asyncio import AsyncIOMotorClient

config = Config()

print(config.mongodb_uri)
print(config.mongodb_db)
print(config.redis_uri)

origins = ["*"]

app = FastAPI(title="DSLink API",
            version=config.version,
            description="A RESTful API for DSLink"
            )

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  
    allow_headers=["*"],  
)
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

databaseClient = AsyncIOMotorClient(config.mongodb_uri)
database = databaseClient[config.mongodb_db]
redisClient = redis.Redis.from_url(config.redis_uri)
logging.info("Database connection established")

async def checkLinksIndex():   
    indexes_cursor = database.links.list_indexes()
    indexes = await indexes_cursor.to_list(length=None)  
    index_names = [index["name"] for index in indexes]
    if not "expiration_time" in index_names:
        await database.links.create_index([("expiration_time", pymongo.ASCENDING)], expireAfterSeconds=0)
        logging.info("Index created")

async def checkCollections():
    collections = await database.list_collection_names()
    if "links" not in collections:
        await database.create_collection("links")
    if "system" not in collections:
        await database.create_collection("system")

async def checkSystemDocument():
    statistic_document = await database.system.find_one({"type":"statistic"})
    if not statistic_document:
        await database.system.insert_one({
            "type":"statistic",
            "route":{
                "api":{
                    "/generate":{
                        "sucess":0,
                        "fail":0
                        },
                    "/lookup":{
                        "sucess":0,
                        "fail":0
                    },
                    "/health":0,
                    "/info":0,
                    "/statistic":0
                    },
                "web":{
                    "redirect":{
                        "sucess":0,
                        "fail":0
                    }
                }
            }
            })

async def closeDB():
    databaseClient.close()
    await redisClient.close()
    logging.info("Database connection closed")

@app.on_event("startup")
async def startup_event():
    await checkLinksIndex()
    await checkCollections()
    await checkSystemDocument()
    logging.info("Database connection established")

@app.on_event("shutdown")
async def shutdown_event():
    await closeDB()

from router.urls import urls
from router.api import api
app.include_router(urls)
app.include_router(api,prefix="/api")

