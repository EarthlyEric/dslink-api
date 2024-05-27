import json
import os

class Config:
    def __init__(self):
        self.config_path = 'config.json'
        self.config = json.load(open(self.config_path,encoding='utf-8'))

        self.version = self.config['version']
        
       