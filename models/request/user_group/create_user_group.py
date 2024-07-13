from pydantic import BaseModel


class CreateUserGroup(BaseModel):
    user_group_id: int
    name: str
    level: int
