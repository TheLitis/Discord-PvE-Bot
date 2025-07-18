import discord
from discord.ext import commands
from config import TOKEN, PREFIX
from database import init_db
from commands.start import Start
from commands.level import Level
from commands.inventory import Inventory
from commands.quest import Quest
from commands.pve_event import PveEvent
from events.on_ready import OnReady

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Инициализация базы данных
init_db()

# Добавление команд и событий
bot.add_cog(Start(bot))
bot.add_cog(Level(bot))
bot.add_cog(Inventory(bot))
bot.add_cog(Quest(bot))
bot.add_cog(PveEvent(bot))
bot.add_cog(OnReady(bot))

# Запуск бота
bot.run(TOKEN)