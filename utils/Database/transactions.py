from sqlalchemy.exc import NoResultFound
from sqlmodel import select

from utils.Database.mapping import User
from sqlmodel.sql.expression import Select, SelectOfScalar
from utils.Database import async_session

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore


# async def fetch_birthday(user_id) -> Birthdays:
#     try:
#         data = await Birthdays.query.fetch(Birthdays.id == user_id)
#         if data:
#             return data.one()
#     except NoResultFound:
#         pass


async def fetch_user(user_id: str) -> User:
    try:
        async with async_session() as db:
            data = await db.exec(select(User).where(User.id == user_id))
        if data:
            return data.one()
    except NoResultFound:
        pass
