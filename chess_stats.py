# Welcome to the chess_stats file

# File that creates individual chess statistics objects

import json
import os
import requests
import re
from datetime import datetime 
from datetime import time
from pytz import timezone
from pprint import pprint
from pytz import timezone
import pytz

class PlayerStats:
    # class that initializes the player object and adds stats to the list
    def __init__(self, name):
        self._name = name
        self._url = "https://api.chess.com/pub/player/"
        self._total_games = []

    def create_directories(self):
        """ Functions that creates folders if they dont already exist """
        path = (f"./graphs/{self._name}")
        time_path = (f"./graphs/{self._name}/time_based")
        opening_path = (f"./graphs/{self._name}/openings")

        # Making folders to save username specific data       
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)

        # Creating Opening graph folder within graphs
        try:
            os.makedirs(opening_path)
        except OSError:
            print("Creation of the directory %s failed" % opening_path)
        else:
            print("Successfully created the directory %s " % opening_path)

        # Creating Time graph folder within graphs
        try:
            os.makedirs(time_path)
        except OSError:
            print("Creation of the directory %s failed" % time_path)
        else:
            print("Successfully created the directory %s" % time_path)


    def query_chess_site(self):
        """ Uses requests.get() to chess.com to return their json archives """
        
        self._query = f"{self._url}{self._name}/games/archives"
        self._archives = requests.get(self._query).json()
        
    def query_archive_chess_site(self, month_url):
        
        """ Loop through the result to get a list of the games """
        monthly_games = requests.get(month_url).json()

        for game in monthly_games['games']:
            game_instance = Chessgame(game)
            print(game_instance.chessgame_to_list())

    def get_archive_url(self):
        return self._archives['archives'][0]

class Chessgame:
    """ An instance of a single game with relevant information """
    
    def __init__(self, game_json):
        self._game_json = game_json
        self._fmt = "%Y.%m.%d %H:%M:%S"
        self._tz = timezone("US/Pacific")
        self._white_name = game_json['white']['username']
        self._white_rating = game_json['white']['rating']
        self._white_result = game_json['white']['result']
        self._black_name = game_json['black']['username']
        self._black_rating = game_json['black']['rating']
        self._black_result = game_json['black']['result']
        self._pgn = game_json['pgn']
        self._eco_code = self.format_eco()
        self._eco_name = self.format_eco_name()
        self._date = self.format_date()
        self._time = self.format_time()
        self._time_control = game_json['time_control']
        self._rules = game_json['rules']
    

    def format_eco(self):
        
        eco1 = re.sub("\W", "", self.get_chessgame_pgn().split('\n')[9].split(" ")[1])
        return eco1

    def format_eco_name(self):
        try:
            eco2 = self.get_chessgame_pgn().split('\n')[10].split("/")[4].split("]")[0]
            eco3 = eco2[:-1]
            eco_name = eco3
        except:
            eco_name = None
        return eco_name

    def format_date(self):
        date1 = self.get_chessgame_pgn().split('\n')[2].split(" ")[1]
        date1 = date1[:-2]
        date1 = date1[1:]
        return date1

    def format_time(self):
        time1 = self.get_chessgame_pgn().split('\n')[12].split(" ")[1]
        time1 = time1[:-2]
        time1 = time1[1:]
    
        if len(time1) == 8: 
            time1 = datetime.strptime(self.format_date() + " " + time1, self._fmt)
            time2 = pytz.utc.localize(time1, is_dst=None).astimezone(self._tz)
            return time2.time()
        else:
            return None

    def get_chessgame_pgn(self):
        return self._pgn

    def chessgame_to_list(self):
        return [self._white_name, self._white_rating, self._white_result, self._black_name, self._black_rating, self._black_result, self._eco_code, self._eco_name, self._date, self._time, self._time_control]

if __name__ == "__main__":
    
    print("Please input your name")
    name_time = input()
    x = PlayerStats(name_time)
    x.query_chess_site()
    x.query_archive_chess_site(x.get_archive_url())

