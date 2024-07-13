import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from db.alembic.BaseDatabase import Base
# from db.alembic.tables.user_group import UserGroup

from datetime import datetime

from sqlalchemy import Integer, String, Date, ForeignKey, DateTime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    """
    A class represents table named "user"

    Table structure
    """
    __tablename__ = "user"
    # Based columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    tel_no: Mapped[str] = mapped_column(String(10))
    date_of_birth: Mapped[str] = mapped_column(Date)
    district: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    province: Mapped[str] = mapped_column(String(25))
    zip_code: Mapped[str] = mapped_column(String(5))
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                  onupdate=func.now())

    # Foreign key
    access_group_id: Mapped[int] = mapped_column(ForeignKey("user_group.id"))

    # Populate data
    from importlib import import_module
    import_module('db.alembic.tables.user_group')
    access_group: Mapped["UserGroup"] = relationship(back_populates="users")

