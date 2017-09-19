""" Demonstration of the various calls to the todo web service.

    server.py must be started separately (and first).

"""
import json
from datetime import datetime

import api
import jsend


def test():
    if 1:
        print("select all tasks")
        result = api.task.select()
        if result["status"] == jsend.SUCCESS:
            data = result["data"]
            for t in data:
                print(json.dumps(t, indent=4))
        else:
            print(json.dumps(result, indent=4))

    if 1:
        print("insert new task")
        result = api.task.insert("this is the summary", "this is the long description")
        print(json.dumps(result, indent=4))
        if result["status"] == jsend.SUCCESS:
            id = result["data"]["id"]
        else:
            id = None

    if 1:
        print("select task {}".format(id))
        result = api.task.select(id)
        print(json.dumps(result, indent=4))
        if "data" in result:
            task = result["data"]
            print(json.dumps(task, indent=4))

    if 1:
        print("update task {} with error".format(id))
        result = api.task.select(id)
        if result["status"] == jsend.SUCCESS:
            task = result["data"]
            result = api.task.update(id, task["summary"], task["description"],
                                     datetime.strptime(task["duedate"], "%Y-%m-%d").date(), "WRONG_STATUS_CODE")
            print(json.dumps(result, indent=4))

    if 1:
        print("update task {}".format(id))
        result = api.task.select(id)
        if result["status"] == jsend.SUCCESS:
            task = result["data"]
            result = api.task.update(id, task["summary"], "changed description",
                                     datetime.strptime(task["duedate"], "%Y-%m-%d").date(), task["status_id"])
            print(json.dumps(result, indent=4))

    if 1:
        print("delete one task")
        result = api.task.delete(id)
        print(json.dumps(result, indent=4))

    if 1:
        print("delete all tasks")
        result = api.task.delete()
        print(json.dumps(result, indent=4))

    if 1:
        print("select one task")
        result = api.task.select(id)
        print(json.dumps(result, indent=4))


if __name__ == "__main__":
    test()
