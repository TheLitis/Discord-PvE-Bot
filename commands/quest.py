from discord.ext import commands
from database import get_connection

class Quest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quests(self, ctx):
        user_id = ctx.author.id
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT level FROM users WHERE id = ?", (user_id,))
        user_level = c.fetchone()[0] if c.fetchone() else 1
        c.execute("SELECT id, description, required_level FROM quests WHERE required_level <= ?", (user_level,))
        quests = c.fetchall()
        conn.close()
        if quests:
            quest_list = "\n".join([f"ID: {q[0]} | {q[1]} (Требуемый уровень: {q[2]})" for q in quests])
            await ctx.send(f"Доступные квесты:\n{quest_list}\n\nИспользуй /take_quest <id> для начала.")
        else:
            await ctx.send("Нет доступных квестов для твоего уровня.")

    @commands.command()
    async def take_quest(self, ctx, quest_id: int):
        user_id = ctx.author.id
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT required_level, description FROM quests WHERE id = ?", (quest_id,))
        quest = c.fetchone()
        if not quest:
            await ctx.send("Квест не найден.")
            return
        required_level, description = quest
        c.execute("SELECT level FROM users WHERE id = ?", (user_id,))
        user_level = c.fetchone()[0] if c.fetchone() else 1
        if user_level < required_level:
            await ctx.send(f"Тебе нужен уровень {required_level} для этого квеста.")
            return
        c.execute("INSERT OR IGNORE INTO user_quests (user_id, quest_id, status, progress) VALUES (?, ?, ?, ?)",
                  (user_id, quest_id, "active", 0))
        conn.commit()
        conn.close()
        await ctx.send(f"{ctx.author.name}, ты взял квест: {description}")

    @commands.command()
    async def quest_progress(self, ctx):
        user_id = ctx.author.id
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT q.description, uq.status, uq.progress FROM user_quests uq "
                  "JOIN quests q ON uq.quest_id = q.id WHERE uq.user_id = ?", (user_id,))
        quests = c.fetchall()
        conn.close()
        if quests:
            progress_list = "\n".join([f"{q[0]} | Статус: {q[1]} | Прогресс: {q[2]}" for q in quests])
            await ctx.send(f"Твои квесты:\n{progress_list}")
        else:
            await ctx.send("У тебя нет активных квестов.")