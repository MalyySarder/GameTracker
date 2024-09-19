import sqlite3

# Создаем или подключаемся к базе данных
def create_connection():
    conn = sqlite3.connect('games.db')
    return conn

# Создаем таблицу, если она не существует
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Добавляем игру в базу данных
def add_game(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO games (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    print("Successfuly added")

# Получаем список всех игр из базы данных
def get_games():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM games')
    games = cursor.fetchall()
    conn.close()
    return [game[0] for game in games]

create_table()