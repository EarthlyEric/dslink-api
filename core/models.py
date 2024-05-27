from pydantic import BaseModel,HttpUrl

class generateSchema(BaseModel):
    url: HttpUrl
    