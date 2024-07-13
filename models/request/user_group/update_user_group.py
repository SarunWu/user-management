from typing import Optional

from pydantic import BaseModel


class UpdateUserGroup(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None

    def is_empty(self):
        return self.name is None and self.level is None
