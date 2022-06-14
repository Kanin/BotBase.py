import asyncio
import logging
import sys

import aiohttp
import discord
from discord.ext.commands import AutoShardedBot as DiscordBot
from utils.Database import async_session

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

        # Argument Handling
        self.debug: bool = any("debug" in arg.lower() for arg in sys.argv)

        # Database
        self.pool = async_session

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
