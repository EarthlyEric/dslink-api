from motor.motor_asyncio import AsyncIOMotorClient


class Database:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.db = client["test"]