from discord.ext import commands
from database import get_connection
from utils.helpers import calculate_xp_for_level

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def level(self, ctx):
        user_id = ctx.author.id
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT level, xp, gold FROM users WHERE id = ?", (user_id,))
        result = c.fetchone()
        conn.close()
        if result:
            level, xp, gold = result
            xp_needed = calculate_xp_for_level(level + 1)
            await ctx.send(f"{ctx.author.name}, твой уровень: {level}\nОпыт: {xp}/{xp_needed}\nЗолото: {gold}")
        else:
            await ctx.send("Ты ещё не начал игру! Используй /start")