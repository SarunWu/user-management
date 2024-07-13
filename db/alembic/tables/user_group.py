import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from db.alembic.BaseDatabase import Base
from datetime import datetime

from sqlalchemy import Integer, String, Date, ForeignKey, DateTime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class UserGroup(Base):
    """
    Class representing a table named "user_group".

    Table Structure:

        ______________________________________________
        | Columns         | Type     | Key | Example |
        |-----------------|----------|-----|---------|
        | id              | int      | PK  | 1       |
        | name            | str[20]  | -   | admin   |
        | level           | int      | -   | 3       |
        | create_date     | datetime | -   |         |
        | update_date     | datetime | -   |         |

    Pre-defined User Groups:
        The higher the level, the more access rights.

        ________________________
        | id | name    | level |
        |----|---------|-------|
        | 1  | admin   | 3     |
        | 2  | vip     | 2     |
        | 3  | common  | 1     |
    """

    __tablename__ = "user_group"

    # Based columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String[20])
    level: Mapped[int] = mapped_column(Integer)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                  onupdate=func.now())

    # populate data for children table #User
    # back_populates = "<the receiver variable in target table>"
    from importlib import import_module
    import_module('db.alembic.tables.user')
    users: Mapped[List["User"]] = relationship(back_populates="access_group")
