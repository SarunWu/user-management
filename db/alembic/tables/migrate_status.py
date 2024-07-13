import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from db.alembic.BaseDatabase import Base

from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class MigrateStatus(Base):
    __tablename__ = "migrate_status"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_file_name: Mapped[str] = mapped_column(String[100])
    target_table: Mapped[str] = mapped_column(String[15])
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
