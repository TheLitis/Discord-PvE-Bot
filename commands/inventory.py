from discord.ext import commands
from database import get_connection

class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def inventory(self, ctx):
        user_id = ctx.author.id
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT i.name, inv.quantity, i.rarity, i.stats FROM inventory inv "
                  "JOIN items i ON inv.item_id = i.id WHERE inv.user_id = ?", (user_id,))
        items = c.fetchall()
        conn.close()
        if items:
            inventory_list = "\n".join([f"{item[0]} ({item[2]}) - {item[1]} шт. | {item[3]}" for item in items])
            await ctx.send(f"{ctx.author.name}, твой инвентарь:\n{inventory_list}")
        else:
            await ctx.send("Твой инвентарь пуст.")

    @commands.command()
    async def use(self, ctx, item_name: str):
        user_id = ctx.author.id
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT inv.item_id, inv.quantity, i.type, i.stats FROM inventory inv "
                  "JOIN items i ON inv.item_id = i.id WHERE inv.user_id = ? AND i.name = ?",
                  (user_id, item_name))
        item = c.fetchone()
        if item and item[1] > 0:
            item_id, quantity, item_type, stats = item
            if item_type == "consumable":
                c.execute("UPDATE inventory SET quantity = quantity - 1 WHERE user_id = ? AND item_id = ?",
                          (user_id, item_id))
                c.execute("DELETE FROM inventory WHERE user_id = ? AND item_id = ? AND quantity <= 0",
                          (user_id, item_id))
                conn.commit()
                await ctx.send(f"{ctx.author.name}, ты использовал {item_name}. Эффект: {stats}")
            else:
                await ctx.send(f"{item_name} нельзя использовать напрямую.")
        else:
            await ctx.send("У тебя нет этого предмета или он закончился.")
        conn.close()