import json
import os
import time
from collections import defaultdict

GAME_TIME_FILE = 'game_time.json'
DATE_TIME_FILE = 'game_time_by_date.json'

# Загрузка данных из файла
def load_game_data():
    if os.path.exists(GAME_TIME_FILE):
        with open(GAME_TIME_FILE, 'r') as f:
            return json.load(f)
    return {}
def load_date_data():
    if os.path.exists(DATE_TIME_FILE):
        with open(DATE_TIME_FILE, 'r') as f:
            return json.load(f)
    return {}

# Сохранение данных в файл
def save_game_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Обновление времени игры в файле
def update_game_time(process_name, session_time):
    data = load_game_data()
    date_data = load_date_data()
    if process_name in data:
        data[process_name]['total_time'] += session_time
        if (data[process_name]['last_played'].split(' ')[0] != time.strftime('%Y-%m-%d')):
            if time.strftime('%Y-%m-%d') not in data:
                # Если даты нет, создаем новую запись для сегодняшней даты
                date_data[time.strftime('%Y-%m-%d')] = {}
            data[process_name]['total_time']=0
            data[process_name]['last_played'] = time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            data[process_name]['last_played'] = time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        data[process_name] = {
            'total_time': session_time,
            'last_played': time.strftime('%Y-%m-%d %H:%M:%S')
        }

    save_game_data(data, GAME_TIME_FILE)

# Разделение данных по датам
def split_data_by_date():
    data = load_game_data()

    date_data = load_date_data()#defaultdict(lambda: {'total_time': 0.0, 'games': {}})
    for game, info in data.items():
        flag = 0
        print(game,info)
        last_played_date = info['last_played'].split(' ')[0]
        if last_played_date:
            if time.strftime('%Y-%m-%d') not in date_data:
                # Если даты нет, создаем новую запись для сегодняшней даты
                date_data[time.strftime('%Y-%m-%d')] = {}
            else:
                if game not in date_data[last_played_date]:
                    print("KAK TAK")
                    date_data[last_played_date][game] = info['total_time']
                    #date_data[last_played_date][game] += info['total_time']
    #save_game_data(data,GAME_TIME_FILE)
    save_game_data(date_data, DATE_TIME_FILE)

# Пример использования
if __name__ == "__main__":
    # Обновление времени игры
    process_name = "game_process_name"  # Название процесса игры, без пути
    session_time = 120  # Время в минутах, например
    update_game_time(process_name, session_time)
    print(f"Время для {process_name} обновлено!")

    # Разделение данных по датам
    split_data_by_date()
    print("Данные разделены по датам и сохранены в файле!")
