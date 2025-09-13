from discord.ext import commands
from database import get_connection
from models.user import User

class Start(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        user_id = ctx.author.id
        user_name = ctx.author.name
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO users (id, name, level, xp, gold) VALUES (?, ?, ?, ?, ?)", 
                  (user_id, user_name, 1, 0, 50))
        c.execute("INSERT OR IGNORE INTO inventory (user_id, item_id, quantity) VALUES (?, ?, ?)",
                  (user_id, 1, 1))  # Даём игроку Меч новичка
        conn.commit()
        conn.close()
        await ctx.send(f"{user_name}, добро пожаловать в мир Эймерии! Ты — начинающий искатель приключений. "
                       f"Твой путь начинается с простого меча и 50 золотых. Используй /quests, чтобы найти задание!")