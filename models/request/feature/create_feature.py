import datetime

from pydantic import BaseModel


class CreateFeature(BaseModel):
    name: str
    level: int
