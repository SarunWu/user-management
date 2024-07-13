from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    tel_no: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    district: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    zip_code: Optional[str] = None
    access_group_id: Optional[int] = None

    def is_empty(self):
        return (self.first_name is None
                and self.last_name is None
                and self.tel_no is None
                and self.date_of_birth is None
                and self.district is None
                and self.city is None
                and self.province is None
                and self.zip_code is None
                and self.access_group_id is None)
