from pydantic import BaseModel


class TableSummary(BaseModel):
    name: str
    description: str
    total_records: int
