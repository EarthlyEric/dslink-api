import json
import os

class Config:
    def __init__(self):
        self.config_path = 'config.json'
        try:
            self.config = json.load(open(self.config_path,encoding='utf-8'))
        except FileNotFoundError:
            print("Config file not found ! Please edit a config.example.json file in the root directory")
            exit(1)
        self.version = str(self.config['version'])
<<<<<<< HEAD

        self.mongodb_uri = os.getenv('MONGODB_URI')
        self.mongodb_db = str(os.getenv('MONGODB_DB'))
        self.redis_uri = str(os.getenv('REDIS_URI'))
        self.buildid = str(os.getenv('BUILD_ID'))
        
        if self.mongodb_uri is None:
            self.mongodb_uri = self.config['connections']['mongodb']['uri']
        if self.mongodb_db is None:
            self.mongodb_db = self.config['connections']['mongodb']['database']
        if self.redis_uri is None:
            self.redis_uri = self.config['connections']['redis']['uri']
       
=======
        self.mongodb_uri = self.config['connections']['mongoDB']['uri']
        self.mongodb_db = self.config['connections']['mongoDB']['database']
        self.redis_uri = self.config['connections']['redis']['uri']
       
>>>>>>> 08f397e59e42fe92a4df9d5a2b60e362facf3d1a
