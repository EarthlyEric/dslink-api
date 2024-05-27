from pydantic import BaseModel
from pydantic import HttpUrl

class generateSchema(BaseModel):
    url: HttpUrl
    