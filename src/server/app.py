from flask import Flask, render_template
from flask_socketio import SocketIO
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

# import socket that updates client and fetches api keys etc
# app is imported in appSocket.py and here serverd. so other middleware has to be applied before
from appSocket.socket import socket_

# # if __name__ == "__main__":
# #     app.run(host='0.0.0.0', port=8080, debug=True)



# recreated server based on socketIO.run which does not work
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication

# If using PyCharm enable Gevent debugging support under:
#   Settings->Build, Execution, Deployment->Python Debugger
# from gevent import monkey
# monkey.patch_all()


# TODO: analyze socketIO.run eg with async_mode "gevent". its very similar so idk y it bugs.
# works for now, for production needs to be refactored anyways so it can run with eg. gunicorn this vid might be helpful:
# https://www.youtube.com/watch?v=tHQvTOcx_Ys 
def run_server():
    application = DebuggedApplication(app)

    server = pywsgi.WSGIServer(('0.0.0.0', 5000), application,handler_class=WebSocketHandler)
    server.serve_forever()

if __name__ == "__main__":
    run_with_reloader(run_server)
