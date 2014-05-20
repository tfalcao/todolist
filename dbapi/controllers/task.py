__author__ = 'cody'

from dbapi import app, db_session
from dbapi.models import *
from utils.rest_api_utils import rest_jsonify

@app.route("/task/<id>", methods=["GET"])
def get_task(id):
    task = db_session.query(Task).filter(Task.id == id).scalar()
    return rest_jsonify(task)