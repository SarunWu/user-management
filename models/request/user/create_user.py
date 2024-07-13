import datetime

from pydantic import BaseModel


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    tel_no: str
    date_of_birth: datetime.datetime
    district: str
    city: str
    province: str
    zip_code: str
    access_group_id: int
