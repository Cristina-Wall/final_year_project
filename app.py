# app.py

from flask import Flask, render_template
from myscript import my_function

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['GET'])
def run_script():
    my_function()
    return 'Script executed successfully'

if __name__ == '__main__':
    app.run(debug=True)
