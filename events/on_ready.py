from discord.ext import commands
from database import populate_initial_data

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        populate_initial_data()
        print(f'Бот {self.bot.user.name} подключён!')