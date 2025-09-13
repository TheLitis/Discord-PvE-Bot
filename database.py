import sqlite3
from config import DB_NAME

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Таблица пользователей
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, name TEXT, level INTEGER, xp INTEGER, gold INTEGER)''')
    # Таблица инвентаря
    c.execute('''CREATE TABLE IF NOT EXISTS inventory 
                 (user_id INTEGER, item_id INTEGER, quantity INTEGER)''')
    # Таблица предметов
    c.execute('''CREATE TABLE IF NOT EXISTS items 
                 (id INTEGER PRIMARY KEY, name TEXT, type TEXT, stats TEXT, rarity TEXT, value INTEGER)''')
    # Таблица квестов
    c.execute('''CREATE TABLE IF NOT EXISTS quests 
                 (id INTEGER PRIMARY KEY, description TEXT, reward TEXT, required_level INTEGER)''')
    # Таблица активных квестов пользователей
    c.execute('''CREATE TABLE IF NOT EXISTS user_quests 
                 (user_id INTEGER, quest_id INTEGER, status TEXT, progress INTEGER)''')
    conn.commit()
    conn.close()

def populate_initial_data():
    conn = get_connection()
    c = conn.cursor()
    # Добавляем начальные предметы
    c.execute("INSERT OR IGNORE INTO items (id, name, type, stats, rarity, value) VALUES (?, ?, ?, ?, ?, ?)",
              (1, "Меч новичка", "weapon", "damage:5", "common", 10))
    c.execute("INSERT OR IGNORE INTO items (id, name, type, stats, rarity, value) VALUES (?, ?, ?, ?, ?, ?)",
              (2, "Зелье здоровья", "consumable", "heal:20", "common", 5))
    c.execute("INSERT OR IGNORE INTO items (id, name, type, stats, rarity, value) VALUES (?, ?, ?, ?, ?, ?)",
              (3, "Кольцо силы", "accessory", "strength:3", "rare", 50))
    # Добавляем начальные квесты
    c.execute("INSERT OR IGNORE INTO quests (id, description, reward, required_level) VALUES (?, ?, ?, ?)",
              (1, "Убей 5 волков в лесу", "xp:50,gold:20,item:2", 1))
    c.execute("INSERT OR IGNORE INTO quests (id, description, reward, required_level) VALUES (?, ?, ?, ?)",
              (2, "Найди потерянное кольцо в пещере", "xp:100,gold:50,item:3", 3))
    conn.commit()
    conn.close()