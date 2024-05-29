import dns.resolver
import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from core.config import Config

config = Config()

origins = [
    "http://localhost",
    "http://localhost:3000"
]

app = FastAPI(title="DSLink API",
            version=config.version,
            description="A RESTful API for DSLink",
            docs_url="/docs",
            redoc_url=None
            )

app.mount("/static", StaticFiles(directory="web/static",html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Adjust the allowed methods as needed
    allow_headers=["*"],  # You can adjust this according to your requirements
)

dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

databaseClient = AsyncIOMotorClient(config.mongodb_uri)
database = databaseClient[config.mongodb_db]



redisClient = redis.Redis.from_url(config.redis_uri)

from router.urls import urls
from router.api import api
app.include_router(urls)
app.include_router(api,prefix="/api")

