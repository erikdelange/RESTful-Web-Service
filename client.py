""" UI server to maintain a todo list.

Usage:
    Start client app via the terminal: > start python client.py
    Then browse to localhost:8080 to open the UI.
"""
from datetime import datetime

from bottle import Bottle, redirect, request, template

import api.task
import jsend

app = Bottle()


@app.get("/")
@app.get("/app")
@app.get("/app/list")
def task_list():
    result = api.task.select()
    if result["status"] == jsend.SUCCESS:
        return template("list", tasks=result["data"])
    else:
        return template("error", result=result)


@app.route("/app/new", method=["GET", "POST"])
def task_new():
    if request.method == "GET":
        return template("new")
    else:  # POST
        summary = request.forms.summary
        description = request.forms.description
        duedate = datetime.strptime(request.forms.duedate, "%Y-%m-%d").date()
        result = api.task.insert(summary, description, duedate, "O")
        if result["status"] == jsend.SUCCESS:
            redirect("/app/list")
        else:
            return template("error", result=result)


@app.route("/app/edit/<task_id:int>", method=["GET", "POST"])
def task_edit(task_id):
    if request.method == "GET":
        result = api.task.select(task_id)
        if result["status"] == jsend.SUCCESS:
            return template("edit", id=task_id, task=result["data"])
        else:
            return template("error", result=result)
    else:  # POST
        summary = request.forms.summary
        description = request.forms.description
        duedate = datetime.strptime(request.forms.duedate, "%Y-%m-%d").date()
        status = request.forms.status
        result = api.task.update(task_id, summary, description, duedate, "O" if status == "open" else "C")
        if result["status"] == jsend.SUCCESS:
            redirect("/app/list")
        else:
            return template("error", result=result)


@app.route("/app/delete/<task_id:int>", method=["GET", "POST"])
def task_delete(task_id):
    if request.method == "GET":
        result = api.task.select(task_id)
        if result["status"] == jsend.SUCCESS:
            return template("delete", id=task_id, task=result["data"])
        else:
            return template("error", result=result)
    else:  # POST
        answer = request.forms.answer
        if answer == "yes":
            result = api.task.delete(task_id)
            if result["status"] == jsend.SUCCESS:
                redirect("/app/list")
            else:
                return template("error", result=result)
        else:
            redirect("/app/list")


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True, reloader=True)
