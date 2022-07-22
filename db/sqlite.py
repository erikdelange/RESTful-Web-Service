import collections
import datetime
import logging
import sqlite3

import db

logger = logging.getLogger(__name__)

""" This module can only handle a connection to one database at a time. 
    The connection object for the currently connected database is stored 
    internally in variable _connection. """

_connection: sqlite3.Connection = None

logger.debug(f"SQLite driver version: {sqlite3.version}")
logger.debug(f"SQLite version: {sqlite3.sqlite_version}")
logger.debug(f"parameter style: {sqlite3.paramstyle}")


def adapt_datetime(dt_obj: datetime.datetime) -> str:
    """ Convert datetime object to datetime string in ISO 8601 format.

    :param datetime.datetime dt_obj: Python datetime object
    :return str: datetime value as a string in ISO 8601 format: 2017-06-24 12:00:00
    """
    return dt_obj.isoformat(sep=" ", timespec="seconds")


def convert_datetime(dt_str: bytes) -> datetime.datetime:
    """ Convert datetime string in ISO 8601 format to datetime object.

    :param bytes dt_str: datetime value as a string in ISO 8601 format: 2017-06-24 12:00:00
    :return datetime.datetime: Python datetime object
    """
    return datetime.datetime.strptime(dt_str.decode("utf-8"), "%Y-%m-%d %H:%M:%S")


def adapt_time(tm_obj: datetime.time) -> str:
    """ Convert time object to time string in HH:MM format (note: no seconds).

    :param datetime.datetime.time tm_obj: Python time object
    :return str: time value as a string in HH:MM format: 12:00
    """
    return tm_obj.isoformat(timespec="minutes")


def convert_time(tm_str: bytes) -> datetime.time:
    """ Convert time string in HH:MM format to time object (seconds will default to 00).

    :param bytes tm_str: datetime value as a string in HH:MM format: 12:00
    :return datetime.datetime.time: Python time object
    """
    return datetime.datetime.strptime(tm_str.decode("utf-8"), "%H:%M").time()


# For column with type DATETIME when writing to a database convert datetime objects to datetime strings
sqlite3.register_adapter(datetime.datetime, adapt_datetime)

# For column with type DATETIME when reading from a database convert datetime strings to datetime objects
sqlite3.register_converter("DATETIME", convert_datetime)

# For column with type TIME when writing to a database convert time objects to time strings
sqlite3.register_adapter(datetime.time, adapt_time)

# For column with type TIME when reading from a database convert time strings to time objects
sqlite3.register_converter("TIME", convert_time)

# For column with type BOOLEAN when writing to a database convert booleans to integers
sqlite3.register_adapter(bool, int)

# For column with type BOOLEAN when reading from a database convert integers to booleans
sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))


class ErrorAlreadyConnected(sqlite3.DatabaseError):
    pass


class ErrorNotConnected(sqlite3.DatabaseError):
    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return "not connected to a database"


def connection() -> sqlite3.Connection:
    return _connection


def create(dbname: str = ":memory:") -> None:
    """ Create a new database and open a connection to it.

    :param str dbname: database filename, if not specified create an in-memory database
    :return: None
    :raises: FileExistsError - file with name dbname already exists
    """
    global _connection

    if dbname != ":memory:":
        try:
            with open(dbname, "r+"):
                pass
            raise FileExistsError
        except FileNotFoundError:
            _connection = sqlite3.connect(dbname)  # this call creates the database
            db.close()

    db.connect(dbname)


def connect(dbname: str = ":memory:") -> None:
    """ Open a connection to an existing SQLite database or a new in-memory database.

    :param str dbname: database filename
    :return: None
    :raises: FileNotFoundError - file dbname not found
    :raises: PermissionError - no read and/or write access to file dbname
    :raises: sqlite3.DatabaseError - dbname is not a valid SQLite database
    :raises: ErrorAlreadyConnected - already connected to a database
    """
    global _connection

    if _connection is not None:
        raise ErrorAlreadyConnected(f"already connected to database {name()}")

    if dbname != ":memory:":
        # check if file dbname exists and is not read-only
        with open(dbname, mode="r+"):
            pass
    try:
        _connection = sqlite3.connect(dbname, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        _connection.row_factory = sqlite3.Row  # best use sqlite3.Row, alternatively use namedtuple_factory (6 X slower)
        _connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
        _connection.execute("PRAGMA foreign_keys = ON;")
        _connection.execute("PRAGMA journal_mode = WAL;")  # WAL (faster) or DELETE (slower)
    except sqlite3.Error as e:
        logger.error(f"{__name__}.connect({dbname}): {type(e).__name__} - {e}")
        _connection = None
        raise e

    # for SQL debugging purposes uncomment the next lines
    if logger.getEffectiveLevel() <= logging.DEBUG:
        _connection.set_trace_callback(logger.debug)  # write every executed SQL statement to the logger


def close() -> None:
    global _connection

    if _connection is not None:
        _connection.close()
    _connection = None


def commit() -> None:
    _connection.commit()


def rollback() -> None:
    _connection.rollback()


def execute(sql: str, parameters: tuple = None) -> sqlite3.Cursor:
    """ Execute a query on the connected database.

    :param str sql: SQL query
    :param tuple parameters: query parameters (if any)
    :return sqlite3.Cursor: query results
    :raises: sqlite.ErrorNotConnected - cannot operate on a closed database
    :raises: sqlite3.ProgrammingError - incorrect number of bindings
    :raises: sqlite3.OperationalError - SQL syntax error
    """
    try:
        if _connection is None:
            raise ErrorNotConnected

        return _connection.execute(sql, () if parameters is None else parameters)
    except sqlite3.Error as e:
        logger.error(f"{e.__module__}.{type(e).__name__} - {e}")
        logger.error(f"SQL statement: {sql}")
        if parameters:
            logger.error(f"statement parameters: {parameters}")
        raise e


def executemany(sql: str, seq_of_parameters=None) -> sqlite3.Cursor:
    """ Executes an SQL statement against all parameter sequences or mappings found in sequence seq_of_parameters

    :param str sql: SQL statement
    :param sequence seq_of_parameters: sequence of parameters
    :return: sqlite3.Cursor
    :raises: sqlite.ErrorNotConnected - cannot operate on a closed database
    :raises: sqlite3.ProgrammingError - incorrect number of bindings
    :raises: sqlite3.OperationalError - SQL syntax error
    """
    try:
        if _connection is None:
            raise ErrorNotConnected

        return _connection.executemany(sql, () if seq_of_parameters is None else seq_of_parameters)
    except sqlite3.Error as e:
        logger.error(f"{e.__module__}.{type(e).__name__} - {e}")
        logger.error(f"SQL statement: {sql}")
        raise e


def executescript(sql_script: str) -> sqlite3.Cursor:
    """ Issues a commit and then executes multiple SQL statements.

    :param str sql_script: one or more SQL statements
    :return: sqlite3.Cursor
    :raises: sqlite.ErrorNotConnected - cannot operate on a closed database
    :raises: sqlite3.OperationalError - SQL syntax error
    """
    try:
        if _connection is None:
            raise ErrorNotConnected

        return _connection.executescript(sql_script)
    except sqlite3.Error as e:
        logger.error(f"{e.__module__}.{type(e).__name__} - {e}")
        logger.error(f"SQL script: {sql_script}")
        raise e


def iterate(cursor: sqlite3.Cursor, arraysize: int = 1000) -> sqlite3.Row:
    """ Fetch query results from cursor in chunks of arraysize records.

    Usage: db.iterate(db.execute("SELECT * FROM table"))
    """
    while True:
        rows = cursor.fetchmany(arraysize)
        if not rows:
            break
        for row in rows:
            yield row


def dump(filename: str = "dump.sql") -> None:
    """ Dump the structure and content of the database to a file.

    :param: str filename: script where SQL statements from dump will be saved

    Note that iterdump() generates an exception if the rowfactory
    is a namedtuple_factory, so in this case the database cannot
    be dumped.
    """
    if _connection is None:
        raise ErrorNotConnected

    if _connection.row_factory is not namedtuple_factory:
        with open(filename, "w") as file:
            for line in _connection.iterdump():
                file.write("{0}\n".format(line))
    else:
        logger.warning("Cannot dump database which has namedtuple_factory as row_factory")


def load(filename: str = "dump.sql") -> None:
    """ Load the structure and/or content of a database from a file.

    This function is meant to be used in conjunction with dump().

    :param: str filename: script containing SQL code to create and/or populate tables
    :raises: sqlite.ErrorNotConnected - cannot operate on a closed database
    :raises: FileNotFoundError - filename not found
    :raises: PermissionError - no read access to filename
    """
    if _connection is None:
        raise ErrorNotConnected

    setting = _connection.execute("PRAGMA foreign_keys;").fetchone()
    _connection.execute("PRAGMA foreign_keys = OFF;")
    with open(filename, "r") as file:
        _connection.executescript(file.read())
    _connection.execute("PRAGMA foreign_keys = {};".format(setting['foreign_keys']))


def export_table_to_dsv(table: str, delimiter: str = ";") -> None:
    """ Write contents of a table or view to delimiter separated file 'table.txt'.
        The decimal separator is always a dot. Using .txt forces Excel to use the
        import dialog where you can specify the separator to use.
    """
    import csv

    if _connection is None:
        raise ErrorNotConnected

    rows = _connection.execute(f"SELECT * FROM {table}")
    filename = f"{table}.txt"
    with open(filename, "w", encoding="windows-1252", newline="") as file:
        writer = csv.writer(file, dialect="excel", delimiter=delimiter)
        writer.writerow([i[0] for i in rows.description])  # write headers
        writer.writerows(rows)  # write data


def name():
    """ Return the name of the connected database. """
    if _connection is None:
        raise ErrorNotConnected()

    for dbinfo in _connection.execute("PRAGMA database_list;"):
        if dbinfo['name'] == "main":
            return dbinfo['file'] if dbinfo['file'] != "" else ":memory:"


def namedtuple_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> tuple:
    """ Tuple based access to a database row.

    Allow access to a field in a row via row.field_name, instead of
    row['field_name'] when using sqlite3.Row as row factory, or
    even row[index_of_field] when not using a row factory at all.
    Performance impact: 6 x slower than when using sqlite3.Row
    """
    fields = [col[0] for col in cursor.description]
    Row = collections.namedtuple("Row", fields)
    return Row(*row)
