"""" Database operations on table 'task' """

import logging

import db

logger = logging.getLogger(__name__)


def select(task_id=None):
    sql = "SELECT id, summary, description, duedate, status_id, modified FROM task"

    if task_id is None:
        sql += ";"
        result = db.execute(sql).fetchall()
    else:
        sql += " WHERE id = ?1;"
        result = db.execute(sql, (task_id,)).fetchone()

    logger.debug("{} - parameters{}".format(sql, () if task_id is None else (task_id,)))

    return result


def insert(summary, description=None, duedate=None, status_id=None):
    parameters = [summary]

    sql = "INSERT INTO task(summary"

    if description:
        parameters.append(description)
    else:
        parameters.append("")
    sql += ", description"

    if duedate:
        parameters.append(duedate)
        sql += ", duedate"

    if status_id:
        parameters.append(status_id)
        sql += ", status_id"

    sql += ") VALUES("

    for i in range(1, len(parameters) + 1):
        sql += "?{}{}".format(i, "" if i == len(parameters) else ",")

    sql += ");"

    logger.debug("{} - parameters{}".format(sql, tuple(parameters)))

    with db.connection():
        cursor = db.connection().cursor()
        cursor.execute(sql, tuple(parameters))
        return cursor.lastrowid


def update(task_id, summary=None, description=None, duedate=None, status_id=None):
    parameters = [task_id]

    sql = "UPDATE task SET"

    if summary:
        parameters.append(summary)
        sql += "{} summary = ?{}".format("" if len(parameters) == 2 else ",", len(parameters))

    if description:
        parameters.append(description)
        sql += "{} description = ?{}".format("" if len(parameters) == 2 else ",", len(parameters))

    if duedate:
        parameters.append(duedate)
        sql += "{} duedate = ?{}".format("" if len(parameters) == 2 else ",", len(parameters))

    if status_id:
        parameters.append(status_id)
        sql += "{} status_id = ?{}".format("" if len(parameters) == 2 else ",", len(parameters))

    sql += " WHERE id = ?1;"

    if len(parameters) > 1:
        logger.debug("{} - parameters{}".format(sql, tuple(parameters)))
        with db.connection():
            db.execute(sql, tuple(parameters))
    else:
        logger.warning("UPDATE task {} without values".format(task_id))


def delete(task_id=None):
    sql = "DELETE FROM task"

    if task_id is None:
        sql += ";"
    else:
        sql += " WHERE id = ?1;"

    logger.debug("{} - parameters{}".format(sql, () if task_id is None else (task_id,)))

    with db.connection():
        db.execute(sql, () if task_id is None else (task_id,))
