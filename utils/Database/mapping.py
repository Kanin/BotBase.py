import math

from sqlalchemy.orm import declarative_base
from sqlmodel import Column, String, ForeignKey, Boolean, Date
from datetime import date

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True)

    # def __int__(self):
    #     return int(self.id)
    #
    # def to_dict(self):
    #     return {
    #         "id": self.id
    #     }


class Birthdays(Base):
    __tablename__ = "birthdays"
    id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    birthday = Column(Date, nullable=False)
    announce = Column(Boolean, default=False)

    @property
    def age(self) -> int:
        return math.floor((date.today() - self.birthday).days / 365.25)
