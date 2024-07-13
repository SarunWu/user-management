import datetime
from typing import Optional

from pydantic import BaseModel


class FileMigrateResult(BaseModel):
    table: Optional[str] = None
    file_path: Optional[str] = None
    status: bool
    description: str
    create_date: Optional[datetime.datetime] = None

    def get_status(self) -> bool:
        return self.status

    def get_description(self) -> str:
        return self.description

    def get_create_date(self) -> datetime.datetime:
        return self.create_date
