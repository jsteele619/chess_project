# File that creates individual chess statistics objects

import os
import requests

class PlayerStats:
    # class that initializes the player object and adds stats to the list
    def __init__(self, name):
        self._name = name
        self._url = "https://api.chess.com/pub/player/"

    def create_directories(self):
        """ Functions that creates folders if they dont already exist """
        path = (f"./graphs/{self._name}")
        time_path = (f"./graphs/{self._name}/time_based")
        opening_path = (f"./graphs/{self._name}/openings")

        # Making folders to save username specific data       
        try:
            os.makedirs(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)

        # Creating Opening graph folder within graphs
        try:
            os.makedirs(opening_path)
        except OSError:
            print ("Creation of the directory %s failed" % opening_path)
        else:
            print ("Successfully created the directory %s " % opening_path)

        # Creating Time graph folder within graphs
        try:
            os.makedirs(time_path)
        except OSError:
            print ("Creation of the directory %s failed" % time_path)
        else:
            print ("Successfully created the directory %s " % time_path)

    def query_chess_site(self):
        
        """ Uses requests.get() to chess.com to return their json archives """
        self._query = f"{self._url}{self._name}/games/archives"
        self._archives = requests.get(self._query).json()
        print(self._archives[1])


if __name__ == "__main__":

    name_time = input()
    PlayerStats(name_time)
