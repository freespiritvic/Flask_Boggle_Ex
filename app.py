from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key24'
app.config['TEMPLATES_AUTO_RELOAD'] = True

boggle_game = Boggle()

@app.route('/')
def home():
    """Display game."""

    board = boggle_game.make_board()
    session['board'] = board
    session['guessing'] = []        
    
    topscore = session.get('topscore', 0)
    numplays = session.get('numplays', 0)

    return render_template('base.html', board=board, topscore=topscore, numplays=numplays)

@app.route('/word_check')
def word_check():
    """Check is word is valid or not."""
    
    word = request.args['word']
    if word in session['guessing']:
        return jsonify({'result': 'Already Guessed - Try Again'})
    else:
        board = session['board']
        response_string = boggle_game.check_valid_word(board, word)

        if response_string == 'ok':
            session['guessing'].append(word)
            session['guessing'] = session['guessing']     

        return jsonify({'result': response_string})

@app.route('/game_over', methods=['POST'])
def end_game():
    """Receive the scores, update the amount of times played, and show highest score"""
    
    data = request.get_json()
    score = data['score']
    topscore = session.get('topscore', 0)
    session['topscore'] = max(score, topscore)  
    session['topscore'] = session['topscore']

    numplays = session.get('numplays', 0)
    session['numplays'] = numplays + 1
    session['numplays'] = session['numplays'] 
    
    print(f'Score: {score}, Top Score: {topscore}, Numplays: {numplays}')
    return jsonify('GAME OVER!')

