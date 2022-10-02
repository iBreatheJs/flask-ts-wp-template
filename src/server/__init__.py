from flask import Flask
from .config import Config

# logs
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

import os


app = Flask(__name__)
app.config.from_object(Config)

from server import routes

# production mode config:
ENABLE_MAIL_NOTIFICATIONS = True
ENABLE_LOG_FILE = True

if not app.debug:
    # Email Notification on Errors
    if ENABLE_MAIL_NOTIFICATIONS:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Server error on ' +
                app.config['PROJECT_NAME'],
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
            print("Mail Notifications activated")

    # Log File
    if ENABLE_LOG_FILE:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/main.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info(os.environ.get('PROJECT_NAME') + ' server started')
