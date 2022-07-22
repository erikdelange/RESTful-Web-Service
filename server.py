""" Web service for a manipulating tasks in a todo-list.

For every possible request a handler is defined. The task id (if relevant) is part
of the request URL. Additional data is sent as JSON in the request message body.
Data is returned to the caller as part of the 'data' key in a JSend compliant JSON
structure.

The database with the todo tasks is accessed via calls to db.task.py
Before starting the server a connection to a database must be opened.
In the implementation below an in-memory database is used which is
initialized every time the server is started.

Start the server via the terminal: > start python server.py
"""
import logging.handlers
import sqlite3

from bottle import Bottle, request, response

import db
import jsend

logger = logging.getLogger(__name__)

app = Bottle()


@app.get("/task")
@app.get("/task/<task_id:int>")
def task_get(task_id=None):
    """ Fetch a single task or fetch all tasks.

    :return: JSend compliant object with key 'data' containing a single or a list of tasks

    response status code:
        200 OK - response JSend object  contains task(s) content
        404 Not Found - task task_id not found, response JSend object contains error
        500 Server Internal Error - most likely database error, detailed error information in response JSend object
    """
    logger.info(f"request {request.method} {request.fullpath}")

    response.headers["Content-Type"] = "application/json"
    response.headers["Cache-Control"] = "no-cache"
    try:
        if task_id is None:
            tasks = db.task.select()
            response.status = 200
            return jsend.success(data=[dict(task) for task in tasks])
        else:
            task = db.task.select(task_id)
            if task is None:
                response.status = 404
                return jsend.fail(data=f"task {task_id} not found")
            else:
                response.status = 200
                return jsend.success(data=dict(task))
    except sqlite3.Error as e:
        logger.error(f"exception {type(e).__name__} in task_get({task_id})")
        response.status = 500
        return jsend.error(message="GET task failed", code=type(e).__name__, data=str(e))


@app.put("/task")
@app.put("/task/<task_id:int>")
def task_put(task_id=None):
    """ Update a single task. Updating all tasks not supported.

    :return: JSend compliant object with key 'data' containing the task_id of the updated task

    response status code:
        200 OK - task updated successfully, response JSend object contains task_id
        400 Bad Request - no JSON content in request
        404 Not Found - task task_id not found, response JSend object contains error
        405 Method Not Allowed - PUT on collection not supported
        500 Server Internal Error - most likely database error, detailed error information in response JSend object
    """
    logger.info(f"request {request.method} {request.fullpath}")
    logger.info(f"JSON {request.json}")

    response.headers["Content-Type"] = "application/json"
    try:
        if task_id is None:
            response.status = 405
            return jsend.error(message="PUT on collection not supported")
        else:
            task = db.task.select(task_id)
            if task is None:
                response.status = 404
                return jsend.fail(data=f"task {task_id} not found")
            else:
                data = request.json
                if data is None:
                    response.status = 400
                    return jsend.fail(data="no JSON content")
                else:
                    summary = data["summary"] if "summary" in data else None
                    description = data["description"] if "description" in data else None
                    duedate = data["duedate"] if "duedate" in data else None
                    status_id = data["status_id"] if "status_id" in data else None
                    db.task.update(task_id, summary, description, duedate, status_id)
                    response.status = 200
                    return jsend.success(data={"id": task_id})
    except sqlite3.Error as e:
        logger.error(f"exception {type(e).__name__} in task_get({task_id})")
        response.status = 500
        return jsend.error(message="GET task failed", code=type(e).__name__, data=str(e))


@app.post("/task")
@app.post("/task/<task_id:int>")
def task_post(task_id=None):
    """ Insert a new task.

    :return: JSend compliant object with key 'data' containing the task_id of newly created task

    response status code:
        201 Created - task inserted, response JSend object contains new task task_id
        400 Bad Request - no JSON content in request
        405 Method Not Allowed - insert with predefined task_id not possible
        500 Server Internal Error - most likely database error, detailed error information in response JSend object
    """
    logger.info(f"request {request.method} {request.fullpath}")
    logger.info(f"JSON {request.json}")

    response.headers["Content-Type"] = "application/json"
    try:
        if task_id is None:
            data = request.json
            if data is None:
                response.status = 400
                return jsend.fail(data="no JSON content")
            else:
                summary = data["summary"] if "summary" in data else None
                description = data["description"] if "description" in data else None
                duedate = data["duedate"] if "duedate" in data else None
                status_id = data["status_id"] if "status_id" in data else None
                task_id = db.task.insert(summary, description, duedate, status_id)
                response.status = 201
                return jsend.success(data={"id": task_id})
        else:
            response.status = 405
            return jsend.error(message="POST on task_id not possible")
    except sqlite3.Error as e:
        logger.error(f"exception {type(e).__name__} in task_post({task_id})")
        response.status = 500
        return jsend.error(message="POST task failed", code=type(e).__name__, data=str(e))


@app.delete("/task")
@app.delete("/task/<task_id:int>")
def task_delete(task_id=None):
    """ Delete a single task. Deleting all tasks is not supported.

    :return: JSend compliant object with key 'data' containing the content of the deleted task

    response status code:
        200 OK - task deleted successfully, response JSend object contains deleted tasks content
        404 Not Found - task task_id not found, response message contains error
        405 Method Not Allowed - delete on collection not supported
        500 Server Internal Error - most likely database error, detailed error information in response JSend object
    """
    logger.info(f"request {request.method} {request.fullpath}")

    response.headers["Content-Type"] = "application/json"
    try:
        if task_id is None:
            response.status = 405
            return jsend.error(message="DELETE on collection not supported")
        else:
            task = db.task.select(task_id)
            if task is None:
                response.status = 404
                return jsend.fail(data=f"task {task_id} not found")
            else:
                db.task.delete(task_id)
                response.status = 200
                return jsend.success(data=dict(task))
    except sqlite3.Error as e:
        logger.error(f"exception {type(e).__name__} in task_delete({task_id})")
        response.status = 500
        return jsend.error(message="DELETE task failed", code=type(e).__name__, data=str(e))


HOST = "127.0.0.10"
PORT = 8080

if __name__ == "__main__":
    import os
    import sys

    logFile = os.path.splitext(os.path.basename(sys.argv[0]))[0] + ".log"

    logHandler = logging.handlers.RotatingFileHandler(logFile,
                                                      maxBytes=10000,
                                                      backupCount=1)  # keeps 1 old file

    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.NOTSET,
                        handlers=[logHandler])

    logging.disable(logging.DEBUG)  # Only show messages *above* this level

    DBNAME = ":memory:"  # For persistent storage change to "todo.db"
    SCRIPT = "todo.sql"

    logger.info("start server")

    try:
        is_new_database = False
        logger.info(f"connect to database {DBNAME}")
        db.connect(DBNAME)
        if db.name() == ":memory:":
            is_new_database = True
    except FileNotFoundError as e:
        logger.info(f"database {DBNAME} does not exist, creating new one")
        try:
            db.create(DBNAME)
            is_new_database = True
        except Exception as e:
            logger.exception(f"exception {type(e).__name__} while creating database {DBNAME}")
    except Exception as e:
        logger.exception(f"exception {type(e).__name__} while connecting to database {DBNAME}")
    else:
        if is_new_database:
            logger.info(f"initializing database {DBNAME} using DDL script {SCRIPT}")
            try:
                with open(SCRIPT) as file:
                    db.executescript(file.read())
            except Exception as e:
                logger.exception(f"exception {type(e).__name__} while initializing database {DBNAME}")

        app.run(host=HOST, port=PORT)
