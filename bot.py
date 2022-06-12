import asyncio
import logging
import os
import sys

import aiohttp
import discord
from discord.ext.commands import AutoShardedBot as DiscordBot
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from utils.Database.transactions import fetch_birthday

from config import config


def get_banner():
    banner = open("utils/assets/banner.txt")
    return banner.read()


class Bot(DiscordBot):

    async def setup_hook(self):
        # self.background_task.start()
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def close(self):
        await super().close()
        await self.session.close()

    def __init__(self):
        super().__init__(
            intents=config.intents,
            command_prefix="!"
        )

        loop = asyncio.new_event_loop()
        # Argument Handling
        self.debug: bool = any("debug" in arg.lower() for arg in sys.argv)

        # Database
        async def setup_database():
            logger = logging.getLogger("sqlalchemy.engine.Engine")
            for handler in logger.handlers:
                logger.removeHandler(handler)
            engine = create_async_engine(os.getenv("DATABASE_URL"), future=True, echo=False)
            async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
            return async_session
        database = loop.run_until_complete(setup_database())
        self.pool = database

        async def test():
            async with self.pool() as db:
                user = await fetch_birthday(db=db, user_id="173237945149423619")
                print(user.age)

        loop.run_until_complete(test())

        # Commands/extensions
        self.initial_extensions = [
            "modules.events.ready"
        ]

        # Logging
        discord_log = logging.getLogger("discord")
        discord_log.setLevel(logging.CRITICAL if not self.debug else logging.INFO)
        self.log: logging.Logger = logging.getLogger("bot")
        self.log.info(f"\n{get_banner()}\nLoading....")

        # Config
        self.version = {
            "bot": config.version,
            "python": sys.version.split(" ")[0],
            "discord.py": discord.__version__
        }
