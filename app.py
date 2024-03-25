from flask import Flask, render_template, request, send_file
from markov_chain import make_song
import os

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

    # Generate the song file
    file_name = make_song(instrument, tonality, tempo, key)

    # Send the generated file as a response
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
