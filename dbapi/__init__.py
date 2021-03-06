import flask
import os
import logging
from logging import Formatter
from flask import Flask, current_app
from flask_bcrypt import Bcrypt
from logging.handlers import RotatingFileHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from multiprocessing import Lock
from werkzeug.local import LocalProxy
from utils.config_utils import load_config_object

app = Flask(__name__)
load_config_object(app, "Dbapi")
app.secret_key = app.config["SECRET_KEY"]

log_handler = RotatingFileHandler(os.path.join(app.config["LOG_DIRECTORY"], __name__),
                                  maxBytes=app.config["MAX_LOG_BYTES"], backupCount=1)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(Formatter(app.config["LOG_FORMAT_STRING"]))
app.logger.addHandler(log_handler)

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], convert_unicode=True)

lock = Lock()

def init_db():
    with lock:
        connection = engine.connect()
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=connection))
    return session

def close_db(db_session):
    db_session.flush()
    db_session.commit()
    db_session.close()
    db_session.bind.close()

def get_db_session():
    if hasattr(flask.g, "_db_session"):
        return flask.g._db_session
    else:
        flask.g._db_session = init_db()
    return flask.g._db_session


@app.before_request
def before():
    flask.g.db_session = LocalProxy(get_db_session)

@app.after_request
def after(f):
    close_db(flask.g.db_session)
    return f

app_bcrypt = Bcrypt(app)

from dbapi.controllers.task import *
from dbapi.controllers.user import *
from dbapi.controllers.error import *

from dbapi.models import  *
Base.metadata.create_all(engine)
