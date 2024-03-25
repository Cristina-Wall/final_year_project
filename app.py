# app.py

from flask import Flask, render_template, request
from markov_chain import test_script
from markov_chain import make_song

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    instrument = request.json['instrument']
    tonality = request.json['tonality']
    tempo = request.json['tempo']
    key = request.json['key']
    make_song(instrument, tonality, tempo, key)
    return 'Song Complete!'

if __name__ == '__main__':
    app.run(debug=True)
