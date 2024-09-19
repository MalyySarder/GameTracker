import os
import database

def scan_steam_folder(steam_folder_path):
    game_exes = []
    print(os.walk(steam_folder_path))
    for root, dirs, files in os.walk(steam_folder_path):
        for file in files:
            if file.endswith('.exe'):
                print(file)
                game_exes.append(file)
    return game_exes
def find_steam_games():
    steam_folder_paths = ['D:/SteamLibrary/steamapps/common','C:/Program Files (x86)/Steam/steamapps/common']  # Или другой путь
    for steam_folder_path in steam_folder_paths:
        game_exes = scan_steam_folder(steam_folder_path)
        for exe in game_exes:
            database.add_game(exe)
    print("Success")