from flask import Flask, render_template, request, redirect, url_for
from db import DB
import random

app = Flask(__name__)

USERNAME = ""
TRIES = 0

db = DB()

wanted_number = random.randint(1, 100)
print("wanted number is",wanted_number)
@app.route('/g')
def game():
    print("in game")
    global USERNAME
    my_tasks = {
        "username": USERNAME,
        "highscore": db.get_top_10()
    }
    args = request.args
    print("args",len(args))
    if len(args) > 0:
        global TRIES
        TRIES += 1
        guessed_number = args.get("guessed_number")
        try:
            guessed_number = int(guessed_number)
            if guessed_number > wanted_number:
                task = ["Die gesuchte Nummer ist kleiner als die eingegebene Nummer!","lower.jpg"]
                print("higher",task)
            elif guessed_number < wanted_number:
                task = ["Die gesuchte Nummer ist größer als die eingegebene Nummer!","higher.png"]
                print("lower",task)
            else:
                task = ["Du hast die gesuchte Nummer gefunden!","russian-president-meme.gif"]
                db.add_game(USERNAME, TRIES)
            my_tasks["task"] = task
        except Exception as e:
            print("Execption:",e)
            my_tasks["task"] = ["Du Ficker gib ne Zahl ein!"]
    print("my tasks:",my_tasks)

    return render_template("game.html", tasks=my_tasks, len=len(my_tasks['highscore']))

@app.route("/")
def index():
    if len(request.args) > 0:
        global USERNAME 
        global TRIES
        USERNAME = ""
        TRIES = 0
        USERNAME = request.args.get("username")
        print("username:",USERNAME)
        db.add_player(USERNAME)
        return redirect(url_for("game"))
    return render_template("login.html")