import dns.resolver
import redis
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.config import Config

config = Config()

app = FastAPI(title="DSLink API",
            version=config.version,
            description="A RESTful API for Luminara.",
            docs_url="/docs",
            redoc_url=None
            )

app.mount("/static", StaticFiles(directory="web/static",html=True), name="static")

dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

databaseClient = AsyncIOMotorClient(config.mongodb_uri)
database = databaseClient[config.mongodb_db]

redisClient = redis.Redis.from_url(config.redis_uri)

from router.urls import urls
from router.api import api
app.include_router(urls)
app.include_router(api,prefix="/api")

