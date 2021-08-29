from flask import Flask, render_template
import chess
from play_chess import Valuator
from state import State
app = Flask(__name__)

evaluation = Valuator()

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/move/<path:fen>/')
def get_move(fen):
    #print(depth)
    print("Calculating...")
    board = chess.Board(fen)
    state = State(board)
    value , move = evaluation.get_best_move(state,evaluation)
	#print('{} {: .0f}'.format(move,value))
    
    return '{} {: .0f}'.format(move,value)


@app.route('/test/<string:tester>')
def test_get(tester):
    return tester


if __name__ == '__main__':
    app.run(debug=True)
