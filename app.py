from flask import Flask, render_template, request, redirect, url_for
from db import DB
import random

app = Flask(__name__)

USERNAME = ""

db = DB()

wanted_number = random.randint(1, 100)
print("wanted number is",wanted_number)
@app.route('/game')
def game():
    global USERNAME
    print(USERNAME)
    my_tasks = {
        "username": USERNAME
    }
    args = request.args
    if len(args) > 0:
        guessed_number = args.get("guessed_number")
        try:
            
            guessed_number = int(guessed_number)
            if guessed_number > wanted_number:
                task = ["Eingegebene Nummer ist größer als die gesuchte Nummer!","higher.png"]
            elif guessed_number < wanted_number:
                task = ["Eingegebene Nummer ist kleiner als die gesuchte Nummer!","lower.jpg"]
            else:
                task = ["Du hast die gesuchte Nummer gefunden!","russian-president-meme.gif"]
            my_tasks["task"] = task
        except:
            my_tasks["task"] = ["Du Ficker gib ne Zahl ein!"]
    print(my_tasks)

    return render_template("game.html", tasks=my_tasks)

@app.route("/")
def index():
    if len(request.args) > 0:
        global USERNAME 
        USERNAME = request.args.get("username")
        print("username:",USERNAME)
        db.add_player(USERNAME)
        return redirect(url_for("game"))
    return render_template("login.html")