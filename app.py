import os
from create_map import *
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def render_the_map():
    return render_template('ecmap.html')

if __name__ == '__main__':
    # Create the map if it doesn't exist
    if not os.path.exists('templates/ecmap.html'):
        wrapper()
    # Run the app
    app.run(debug=True)