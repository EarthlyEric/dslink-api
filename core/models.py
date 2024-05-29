from typing import Optional
from pydantic import BaseModel
from pydantic import HttpUrl

class generateSchema(BaseModel):
    url: HttpUrl
    expiryDays: Optional[int] = 7
    anonymous : bool = True

class lookupSchema(BaseModel):
    hash: str

    