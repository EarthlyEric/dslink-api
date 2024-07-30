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
        self.mongodb_uri = self.config['connections']['mongoDB']['uri']
        self.mongodb_db = self.config['connections']['mongoDB']['database']
        self.redis_uri = self.config['connections']['redis']['uri']
        self.buildid = os.getenv('BUILD_ID')
       
