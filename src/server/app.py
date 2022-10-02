from flask import Flask, render_template
from werkzeug import debug

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
# default to main page
# @app.route('/')
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

# import the api eps
from api import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)
