import math

import sqlalchemy as sa
from datetime import date

from utils.Database import Base


class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.String, primary_key=True)

    def __int__(self):
        return int(self.id)

    def to_dict(self):
        return {
            "id": self.id
        }


# class Birthdays(Base):
#     __tablename__ = "birthdays"
#     id = sa.Column(sa.String, sa.ForeignKey("user.id", ondelete="cascade"), primary_key=True)
#     birthday = sa.Column(sa.Date, nullable=False)
#     announce = sa.Column(sa.Boolean, default=False, nullable=False)
#
#     @property
#     def age(self) -> int:
#         return math.floor((date.today() - self.birthday).days / 365.25)
#
#     def __str__(self):
#         return f"{self.birthday}"
#
#     def __repr__(self):
#         return f"<Birthday id={self.id} birthday={self.birthday} announce={self.announce}>"
