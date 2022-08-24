import sqlite3
from sqlite3 import Error
import os

create_players = """ CREATE TABLE IF NOT EXISTS players (
    id integer PRIMARY KEY,
    name text
) """
create_games = """ CREATE TABLE IF NOT EXISTS games (
    id integer PRIMARY KEY,
    player_id integer,
    tries integer
) """
# create_highscore = """ """

class DB:
    conn = None
    cursor = None
    def __init__(self):
        try:
            self.conn = sqlite3.connect("game.db", check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.cursor.execute(create_players)
            self.cursor.execute(create_games)
            self.conn.commit()
        except Error as e:
            print("Failed connecting to database with error",e)

    def add_player(self,name):
        self.cursor.execute(f''' SELECT id FROM players ''')
        # print(self.cursor.fetchall())
        if len(self.cursor.fetchall()) == 0:
            self.cursor.execute(f''' INSERT INTO players (name) VALUES ('{name}') ''')
            print(f"no player with name {name} in table. inserting...")
        self.conn.commit()

    def drop_db(self):
        self.conn.close()
        os.remove("game.db")

# db = DB()
# db.cursor.execute("select * from players")
# print(db.cursor.fetchall())
# db.drop_db()