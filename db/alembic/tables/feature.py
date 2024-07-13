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


class Feature(Base):
    __tablename__ = "feature"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String[50])
    level: Mapped[int] = mapped_column(Integer)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                  onupdate=func.now())
