""" API library for todo list webservice.

Returns a jsend format response as python dictionary

Typical usage:
    result = api.task.select(1234)
    if result["status"] == jsend.SUCCESS then:
            data = result["data"]
            ...
"""

import json
from datetime import date

import requests

import jsend

URL = "http://127.0.0.10:8080"
# URL = "https://kwedelange.pythonanywhere.com"


def select(id=None):
    try:
        if id is None:
            result = requests.get(URL + "/task")
        else:
            result = requests.get(URL + "/task/{:d}".format(id))
        return result.json()
    except Exception as e:
        result = jsend.error("select task failed", code=type(e).__name__, data=str(e))
        return json.loads(result)


def insert(summary="", description="", duedate=date.today(), status_id="O"):
    try:
        result = requests.post(URL + "/task", json=dict(summary=summary, description=description,
                                                        duedate=duedate.isoformat(), status_id=status_id))
        return result.json()
    except Exception as e:
        result = jsend.error("insert task failed", code=type(e).__name__, data=str(e))
        return json.loads(result)


def update(id, summary, description, duedate, status_id):
    try:
        result = requests.put(URL + "/task/{:d}".format(id), json=dict(id=id, summary=summary, description=description,
                                                                       duedate=duedate.isoformat(),
                                                                       status_id=status_id))
        return result.json()
    except Exception as e:
        result = jsend.error("update task failed", code=type(e).__name__, data=str(e))
        return json.loads(result)


def delete(id=None):
    try:
        if id is None:
            result = requests.delete(URL + "/task")
        else:
            result = requests.delete(URL + "/task/{:d}".format(id))
        return result.json()
    except Exception as e:
        result = jsend.error("delete task failed", code=type(e).__name__, data=str(e))
        return json.loads(result)
