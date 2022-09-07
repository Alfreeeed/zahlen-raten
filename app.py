from flask import Flask, render_template, request, redirect, url_for
from db import DB
import random
from waitress import serve

app = Flask(__name__)

USERNAME = ""
TRIES = 0
NUMBER = random.randint(1, 100)
print("wanted number is",NUMBER)

db = DB()

@app.route('/g')
def game():
    global USERNAME
    global TRIES
    global NUMBER
    
    my_tasks = {
        "username": USERNAME,
        "highscore": db.get_top_10()
    }
    args = request.args
    print("args",len(args))
    if len(args) > 0:
        if args.get("action") == "neues_spiel":
            TRIES = 0
            NUMBER = random.randint(1, 100)
            print("wanted number is",NUMBER)
            return redirect(url_for("game"))
        elif args.get("action") == "zum_login":
            NUMBER = random.randint(1, 100)
            print("wanted number is",NUMBER)
            return redirect(url_for("index"))

        guessed_number = args.get("guessed_number")
        try:
            guessed_number = int(guessed_number)
            TRIES += 1
            get_guess_result(guessed_number, my_tasks)
            my_tasks["try"] = TRIES
            my_tasks["pepe"] = get_pepe_img(TRIES)
        except Exception as e:
            print("Execption:",e)
            my_tasks["task"] = ["Du Lappen gib ne Zahl ein!","fake_news.webp"]
            my_tasks["pepe"] = "pepe_das_ist_keine_zahl.png"
    else:
        my_tasks["pepe"] = "pepe_neuer_highscore.png"
    return render_template("game.html", tasks=my_tasks, len=len(my_tasks['highscore']))

@app.route("/")
def index():
    if len(request.args) > 0:
        global USERNAME 
        global TRIES
        TRIES = 0
        USERNAME = ""         
        USERNAME = request.args.get("username")
        print("username:",USERNAME)
        db.add_player(USERNAME)
        return redirect(url_for("game"))
    return render_template("login.html")


def get_pepe_img(versuch):
    count = db.get_pepe_count(versuch)
    if count == 0:
        return "pepe_happy_0.webp"
    elif count in [1,2]:
        return "pepe_happy_1_2.jpg"
    elif count in [3,4]:
        return "pepe_happy_3_4.png"
    elif count in [5,6]:
        return "pepe_happy_5_6.png"
    elif count in [7,8]:
        return "pepe_happy_7_8.png"
    elif count in [9,10]:
        return "pepe_happy_9_10.webp"
    else:
        return "pepe_50_versuche.png"
    
def get_guess_result(guessed_number, my_tasks, test=False):
    if guessed_number > NUMBER:
        my_tasks['task'] = ["Die gesuchte Nummer ist kleiner als die eingegebene Nummer!","lower.jpg"]
    elif guessed_number < NUMBER:
        my_tasks['task'] = ["Die gesuchte Nummer ist größer als die eingegebene Nummer!","higher.png"]
    else:
        my_tasks['task'] = ["Du hast die gesuchte Nummer gefunden!","pepe_sieg.gif"]
        if test is False:
            my_tasks['highscore'] = db.get_top_10()
            db.add_game(USERNAME, TRIES)
    

def unit_tests():
    global NUMBER
    NUMBER = 50
    result = {}
    # die eingegebene Nummer ist zu niedrig und muss größer sein
    get_guess_result(4,result,True)
    assert result['task'][1] == 'higher.png'
    # die eingegebene Nummer ist zu groß und muss niedriger sein
    get_guess_result(80,result,True)
    assert result['task'][1] == 'lower.jpg'
    # die gesuchte Nummer wurde gefunden
    get_guess_result(50,result,True)
    assert result['task'][1] == 'pepe_sieg.gif'

serve(app, host='0.0.0.0', port=8080, threads=1)
# unit_tests()
        
