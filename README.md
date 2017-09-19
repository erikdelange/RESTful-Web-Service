# RESTful web service example

Ever wondered how to build a web service and how to actually communicate with it? Then just have a look at this Python project which contains:
- A minimal RESTful web service to maintain a todo list. Only four functions are implemented: retrieving the content of one or all tasks and adding, editing and deleting tasks.
- A minimal web app to view and maintain the todo list, using calls to the web service.

The web service and app are built using the *Bottle* web framework.
All replies from the web service are structured following the *jsend* conventions.
The Bottle web page templates are built on top off the bootstrap framework.

In the project the directory structure for the WEB API and the GUI application server are mixed.
See below the relevant parts for each of them.

##### WEB API server

    db\
        __init__.py
        sqlite.py
        task.py
    jsend.py
    server.py

    todo.db
    todo.sql

The actual web service resides in *server.py*. It connects to the *task* table in the SQLite todo.db database via *db\task.py*. SQL file todo.sql contains the statements needed to create and fill the todo database. When you want to take a look at the database I recommend using freeware SQLite database manager SQLiteStudio.

##### GUI application server

    api\
        __init__.py
        task.py
    views\
        *.tpl
    jsend.py
    client.py

File *client.py* contains the app server. Calls to the web service are made via *api\task.py*. Directory *views* contains the html code of the various web pages.

To run the server and the GUI use the Windows command prompt or the powershell:
```
> start python server.py
> start python client.py
```
The server listens to address 127.0.0.10:8080 and the client to 127.0.0.1:8080.
If database todo.db does not exist it will automatically be created the first time server.py is run.

To view the GUI start your webbrowser and browse to 127.0.0.1:8080.
 