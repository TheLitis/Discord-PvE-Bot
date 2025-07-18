import random
import json
import logging
import asyncio
from discord import app_commands
from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from utils.db import AsyncSessionLocal
from models import User, Item, Quest, Inventory, UserQuest

logger = logging.getLogger(__name__)

class Pve(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # загрузка игровых данных
        self.items = self._load_json('data/items.json')
        self.quests = self._load_json('data/quests.json')
        self.events = self._load_json('data/events.json')

    def _load_json(self, path: str):
        with open(path, encoding='utf-8') as f:
            return json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        # при первом входе загружаем справочные данные в БД
        async with AsyncSessionLocal() as session:
            for it in self.items:
                exists = (await session.execute(select(Item).where(Item.id == it['id']))).scalar_one_or_none()
                if not exists:
                    session.add(Item(id=it['id'], name=it['name'], description=it.get('description', '')))
            for q in self.quests:
                exists = (await session.execute(select(Quest).where(Quest.id == q['id']))).scalar_one_or_none()
                if not exists:
                    session.add(Quest(id=q['id'], title=q['title'], description=q.get('description',''), xp_reward=q.get('xp_reward',0)))
            await session.commit()
        logger.info('Reference data loaded into DB')

    @app_commands.command(name='start', description='Зарегистрировать игрока')
    async def start(self, interaction: commands.Interaction):
        async with AsyncSessionLocal() as session:
            user = await session.get(User, interaction.user.id)
            if user:
                await interaction.response.send_message('Вы уже зарегистрированы.')
                return
            new_user = User(id=interaction.user.id, name=interaction.user.name)
            session.add(new_user)
            await session.commit()
            await interaction.response.send_message('Добро пожаловать в PvE-бот!')

    @app_commands.command(name='inventory', description='Показать инвентарь')
    async def inventory(self, interaction: commands.Interaction):
        async with AsyncSessionLocal() as session:
            user = await session.get(User, interaction.user.id)
            if not user:
                await interaction.response.send_message('Сначала используйте /start')
                return
            inv = (await session.execute(select(Inventory).where(Inventory.user_id == user.id))).scalars().all()
            if not inv:
                await interaction.response.send_message('Инвентарь пуст.')
                return
            msg = "".join(f"{item.item.name}: {item.quantity}" for item in inv)
            await interaction.response.send_message(f"Инвентарь:{msg}")

    @app_commands.command(name='pve', description='Запустить PvE-событие')
    async def pve(self, interaction: commands.Interaction):
        async with AsyncSessionLocal() as session:
            user = await session.get(User, interaction.user.id)
            if not user:
                await interaction.response.send_message('Сначала зарегистрируйтесь через /start')
                return
            event = random.choice(self.events)
            success = random.random() > 0.3
            result = 'победили!' if success else 'проиграли.'
            xp_delta = event.get('xp', 10) if success else 0
            user.xp += xp_delta
            if user.xp >= user.level * 100:
                user.level += 1
                user.xp = 0
                lvl_msg = f" Поздравляем! Вы достигли уровня {user.level}."
            else:
                lvl_msg = ''
            session.add(user)
            await session.commit()
            await interaction.response.send_message(f"Событие: {event['name']} — вы {result}{lvl_msg} (+{xp_delta} XP)")
            logger.info(f"User {user.id} ran event {event['id']} result={success}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Pve(bot))

# Добавляем команды для квестов ниже предыдущих

    @app_commands.command(name='take_quest', description='Взять квест')
    async def take_quest(self, interaction: commands.Interaction, quest_id: int):
        async with AsyncSessionLocal() as session:
            user = await session.get(User, interaction.user.id)
            if not user:
                return await interaction.response.send_message('Сначала используйте /start')
            quest = await session.get(Quest, quest_id)
            if not quest:
                return await interaction.response.send_message('Квест не найден.')
            exists = await session.get(UserQuest, (user.id, quest.id))
            if exists:
                return await interaction.response.send_message('Вы уже взяли этот квест.')
            user_quest = UserQuest(user_id=user.id, quest_id=quest.id)
            session.add(user_quest)
            await session.commit()
            await interaction.response.send_message(f'Квест "{quest.title}" взят!')

    @app_commands.command(name='quest_progress', description='Показать прогресс по квесту')
    async def quest_progress(self, interaction: commands.Interaction, quest_id: int):
        async with AsyncSessionLocal() as session:
            uq = await session.get(UserQuest, (interaction.user.id, quest_id))
            if not uq:
                return await interaction.response.send_message('У вас нет такого квеста.')
            quest = await session.get(Quest, quest_id)
            await interaction.response.send_message(
                f'Квест: {quest.title}Статус: {uq.status}Прогресс: {uq.progress}/{quest.xp_reward}'
            )