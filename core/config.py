import json
import os

class Config:
    def __init__(self):
        self.config_path = 'config.json'
        self.config = json.load(open(self.config_path,encoding='utf-8'))

        self.version = str(self.config['version'])

        self.mongodb_uri = os.getenv('MONGODB_URI')
        self.mongodb_db = str(os.getenv('MONGODB_DB'))
        self.redis_uri = str(os.getenv('REDIS_URI'))
        
       