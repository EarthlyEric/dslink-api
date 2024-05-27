import string
import random
from core.config import Config

config = Config()

class utils:
    @staticmethod
    def generateHash(legth:int=8):
        characters = string.ascii_letters + string.digits
        hash = ''.join(random.choices(characters, k=legth))
        
        return hash


