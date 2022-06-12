from sqlalchemy.exc import NoResultFound
from sqlmodel import select
from utils.Database.mapping import User, Birthdays
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore


def select_user_by_id(user_id: str):
    return select(User).where(User.id == user_id)


async def fetch_birthday(db, user_id) -> Birthdays:
    try:
        data = await db.exec(select(Birthdays).where(Birthdays.id == str(user_id)))
        if data:
            return data.one()
    except NoResultFound:
        pass


async def fetch_user(db, user_id: str | int) -> User:
    try:
        data = (await db.exec(select_user_by_id(str(user_id)))).one()
        if data:
            return data
    except NoResultFound:
        pass
