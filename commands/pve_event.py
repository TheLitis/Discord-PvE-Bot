from discord.ext import commands
import random
from database import get_connection

class PveEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pve(self, ctx):
        user_id = ctx.author.id
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT level FROM users WHERE id = ?", (user_id,))
        user_level = c.fetchone()[0] if c.fetchone() else 1

        events = [
            {"name": "Битва с волком", "desc": "Ты встретил дикого волка!", "xp": 20, "gold": 10, "item": None, "difficulty": 1},
            {"name": "Сундук в лесу", "desc": "Ты нашёл старый сундук.", "xp": 10, "gold": 15, "item": 2, "difficulty": 1},
            {"name": "Засада гоблинов", "desc": "Группа гоблинов напала на тебя!", "xp": 50, "gold": 25, "item": None, "difficulty": 3},
            {"name": "Таинственный алтарь", "desc": "Ты обнаружил древний алтарь с сокровищами.", "xp": 30, "gold": 50, "item": 3, "difficulty": 5}
        ]
        
        available_events = [e for e in events if user_level >= e["difficulty"]]
        event = random.choice(available_events if available_events else events[:1])
        
        # Обновление пользователя
        c.execute("UPDATE users SET xp = xp + ?, gold = gold + ? WHERE id = ?", (event["xp"], event["gold"], user_id))
        if event["item"]:
            c.execute("INSERT INTO inventory (user_id, item_id, quantity) VALUES (?, ?, 1) "
                      "ON CONFLICT (user_id, item_id) DO UPDATE SET quantity = quantity + 1", (user_id, event["item"]))
        
        # Проверка квестов
        c.execute("UPDATE user_quests SET progress = progress + 1 WHERE user_id = ? AND quest_id = 1 AND status = 'active'", (user_id,))
        conn.commit()
        conn.close()

        response = f"{ctx.author.name}, событие: {event['desc']}\nНаграда: {event['xp']} XP, {event['gold']} золота"
        if event["item"]:
            response += f", предмет (ID: {event['item']})"
        await ctx.send(response)