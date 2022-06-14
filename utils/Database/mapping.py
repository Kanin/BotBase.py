import sqlalchemy as sa

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
