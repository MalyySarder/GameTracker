import time
import psutil
import tkinter as tk
import threading
from data_manager import update_game_time, split_data_by_date
from database import get_games,add_game
from tkcalendar import DateEntry
import json
import os
from games_finder import find_steam_games
GAME_TIME_BY_DATE_FILE = 'game_time_by_date.json'

# Задержка между проверками процессов
CHECK_INTERVAL = 15  # Проверка каждую минуту

# Переменные для управления отслеживанием
is_paused = False
is_tracking = False

def filter_similar_games(game_list):
    game_list = sorted(game_list, key=len)
    print(game_list)
    for i, game in enumerate(game_list):
        for other_game in game_list[i + 1:]:
            if other_game.startswith(game[:-4]):  # Если начинается одинаково, удаляем длинную версию
                game_list.pop(game_list.index(other_game))
    print(game_list)
    return game_list

def track_game_time():
    global is_tracking, is_paused
    print("Начинаем отслеживать время игр...")
    games_processes = filter_similar_games(get_games())  # Получаем список процессов игр из БД

    while is_tracking:
        if not is_paused:
            active_processes = [p.name() for p in psutil.process_iter()]
            for game in games_processes:
                if game in active_processes:
                    print(f"Игра {game} запущена. Обновляем время...")
                    session_time = CHECK_INTERVAL / 60  # Время в минутах
                    split_data_by_date()
                    update_game_time(game, session_time)

        time.sleep(CHECK_INTERVAL)

def start_tracking():
    global is_tracking
    if not is_tracking:
        is_tracking = True
        threading.Thread(target=track_game_time, daemon=True).start()
        update_status("Отслеживание началось")

def pause_tracking():
    global is_paused
    is_paused = not is_paused
    pause_button.config(text="Продолжить" if is_paused else "Пауза")
    update_status("Отслеживание на паузе" if is_paused else "Отслеживание продолжается")

def stop_tracking():
    global is_tracking
    is_tracking = False
    update_status("Отслеживание остановлено")

def update_status(message):
    status_label.config(text=message)

root1 = tk.Tk()
root1.iconify()
report_text = ""
def start_report_gen():
    def load_data(filename):
        """Загружает данные из файла."""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return {}

    def generate_report(date):
        """Генерирует отчет по играм за указанную дату."""
        data = load_data(GAME_TIME_BY_DATE_FILE)
        if date in data:
            games = data[date]
            total_time = 0
            for game in games:
                total_time += data[date][game]
            report = f"Дата: {date}\nОбщее время: {total_time:.2f} мин\n\n"
            for game in games:
                report += f"{game}: {data[date][game]:.2f} мин\n"
        else:
            report = f"Нет данных для выбранной даты: {date}"

        return report

    def show_report():
        """Обработчик кнопки 'Показать отчет'."""
        global date_entry, report_text
        print(date_entry)
        selected_date = date_entry.get_date().strftime('%Y-%m-%d')
        print(selected_date)
        report = generate_report(selected_date)
        print(report)
        report_text.set(report)
        report_text = tk.StringVar()
        report_label = tk.Label(root1, textvariable=report_text, justify=tk.LEFT)
        report_label.pack(pady=10)



    def clear_fields():
        for widget in root1.winfo_children():
            widget.destroy()

    def start_report_gen1():
        clear_fields()
        # Создание главного окна
        root1.title("Генератор отчета по играм")

        # Виджеты для выбора даты
        date_label = tk.Label(root1, text="Выберите дату:")
        date_label.pack(pady=10)

        global date_entry
        date_entry = DateEntry(root1, date_pattern='yyyy-mm-dd')
        print(date_entry.get())
        date_entry.pack(pady=10)

        # Кнопка для генерации отчета
        generate_button = tk.Button(root1, text="Показать отчет", command=show_report)
        generate_button.pack(pady=10)

        # Поле для отображения отчета
        global report_text
        print(report_text)
        report_text = tk.StringVar()
        report_label = tk.Label(root1, textvariable=report_text, justify=tk.LEFT)
        report_label.pack(pady=10)

        # Запуск приложения
        root1.mainloop()

    root1.deiconify()
    start_report_gen1()

# Создаем графический интерфейс
root = tk.Tk()
root.title("Game Tracker")

# Статусное сообщение
status_label = tk.Label(root, text="Готово", font=("Helvetica", 12))
status_label.pack()

#Найти игры из каталогов Steam на ПК
find_button = tk.Button(root, text="Найти Steam-игры", command=find_steam_games)
find_button.pack()

# Таймер управления
start_button = tk.Button(root, text="Старт", command=start_tracking)
start_button.pack()

pause_button = tk.Button(root, text="Пауза", command=pause_tracking)
pause_button.pack()

stop_button = tk.Button(root, text="Остановить", command=stop_tracking)
stop_button.pack()

# Кнопка для генерации отчета
report_button = tk.Button(root, text="Сгенерировать отчет", command=start_report_gen)
report_button.pack()

tk.Label(root, text="Название процесса игры:").pack(pady=10)
entry_game = tk.Entry(root)
entry_game.pack(pady=10)
#name_added_game = entry_game.get()
add_game_button = tk.Button(root, text="Добавить", command=lambda: add_game(entry_game.get()))
add_game_button.pack()


root.mainloop()
