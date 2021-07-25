from flask import Flask, session, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "Panda20Bear35809Gummies"

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

def get_board():
    board = session.get("board", boggle_game.make_board())
    return board

@app.route("/")
def home_page():
    """displays the game board"""
    board = get_board()
    session["board"] = board
    score = session.get("score", 0)
    session["score"] = score
    played = session.get("played", 0)
    session["played"] = played
    return render_template("home.html", board=board, score=score, played=played)

@app.route("/guess")
def guess_word():
    """extracts a word guess & returns result"""
    board = get_board()
    word = request.args.get("word")
    result = boggle_game.check_valid_word(board, word)
    return jsonify({"result": result})

@app.route("/update", methods=["POST"])
def update_stats():
    """extracts score & updates high score, also updates # times played"""
    high_score = session.get("score", 0)
    game_score = request.json["score"]
    if game_score > high_score:
        session["score"] = game_score
    times_played = session.get("played", 0)
    session["played"] = times_played + 1
    return jsonify({"played": session["played"], "score": session["score"]})
