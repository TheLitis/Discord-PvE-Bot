import logging
import asyncio
from discord.ext import commands
from config import Config
from utils.db import init_db

logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

intents = commands.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"Bot ready: {bot.user}")

async def main():
    await init_db()
    # загрузка всех Cogs автоматически
    for extension in ["cogs.pve"]:
        await bot.load_extension(extension)
    await bot.start(Config.TOKEN)

if __name__ == "__main__":
    asyncio.run(main())