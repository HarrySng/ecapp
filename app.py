from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/maritimes')
def maritimes():
    return render_template('maritimes.html')

@app.route('/quebec')
def quebec():
    return render_template('quebec.html')

@app.route('/ontario')
def ontario():
    return render_template('ontario.html')

@app.route('/prairies')
def prairies():
    return render_template('prairies.html')

@app.route('/bc')
def bc():
    return render_template('bc.html')

@app.route('/north')
def north():
    return render_template('north.html')

if __name__ == '__main__':
    app.run(debug=True)