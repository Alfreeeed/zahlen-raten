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
    tries integer,
    finished bool,
    FOREIGN KEY (player_id) REFERENCES players(id)
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
        self.cursor.execute(f""" SELECT id FROM players WHERE name = '{name}'""")
        # print(self.cursor.fetchall())
        if len(self.cursor.fetchall()) == 0:
            self.cursor.execute(f''' INSERT INTO players (name) VALUES ('{name}') ''')
            print(f"no player with name {name} in table. inserting...")
        self.conn.commit()
    
    def add_game(self, player_name, tries, finished=True):
        #(SELECT id FROM players WHERE name = '{player_name}')
        self.cursor.execute(f""" INSERT INTO games (player_id, tries, finished) VALUES ((SELECT id FROM players WHERE name = '{player_name}'), {tries}, {finished}) """)
        self.conn.commit()
    
    def get_top_10(self):
        self.cursor.execute(""" SELECT (SELECT name FROM players WHERE id = player_id), tries FROM games WHERE finished = 1 ORDER BY tries,player_id LIMIT 10 """)
        return self.cursor.fetchall()

    def get_pepe_count(self, versuch):
        self.cursor.execute(f""" SELECT count(*) FROM games WHERE tries < {str(versuch)}""")
        return self.cursor.fetchone()[0]

    def execute(self,query):
        self.cursor.execute(query)

    def drop_db(self):
        self.conn.close()
        os.remove("game.db")

# db = DB()
# print(db.get_top_10())
# db.cursor.execute("select * from players")
# print(db.cursor.fetchall())
# db.drop_db()
# print(db.get_top_10())
# print(db.get_pepe_count(3))
# db.execute(""" UPDATE games SET tries = 420 WHERE player_id = (SELECT id FROM players WHERE name = 'Snoop Dogg')""")
# db.conn.commit()