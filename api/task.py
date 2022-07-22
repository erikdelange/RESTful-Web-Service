""" API library for calling the to-do list webservice.

See server.py for all possible calls.

Returns a JSend compliant response as python dictionary.

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
import server

URL = f"http://{server.HOST}:{server.PORT}"


def select(task_id=None):
    try:
        if task_id is None:
            result = requests.get(URL + "/task")
        else:
            result = requests.get(URL + f"/task/{task_id:d}")
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


def update(task_id, summary, description, duedate, status_id):
    try:
        result = requests.put(URL + f"/task/{task_id:d}",
                              json=dict(task_id=task_id, summary=summary, description=description,
                                        duedate=duedate.isoformat(), status_id=status_id))
        return result.json()
    except Exception as e:
        result = jsend.error("update task failed", code=type(e).__name__, data=str(e))
        return json.loads(result)


def delete(task_id=None):
    try:
        if task_id is None:
            result = requests.delete(URL + "/task")
        else:
            result = requests.delete(URL + f"/task/{task_id:d}")
        return result.json()
    except Exception as e:
        result = jsend.error("delete task failed", code=type(e).__name__, data=str(e))
        return json.loads(result)
