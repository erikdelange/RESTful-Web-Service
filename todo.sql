--
-- File generated with SQLiteStudio v3.1.1 on ma sep 18 11:15:33 2017
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: status
DROP TABLE IF EXISTS status;

CREATE TABLE status (
    id          TEXT PRIMARY KEY
                     CONSTRAINT [status id may not be empty] CHECK (LENGTH(id) > 0),
    description TEXT NOT NULL
                     CONSTRAINT [status description may not be empty] CHECK (LENGTH(description) > 0) 
)
WITHOUT ROWID;

INSERT INTO status (
                       id,
                       description
                   )
                   VALUES (
                       'C',
                       'Closed'
                   );

INSERT INTO status (
                       id,
                       description
                   )
                   VALUES (
                       'O',
                       'Open'
                   );


-- Table: task
DROP TABLE IF EXISTS task;

CREATE TABLE task (
    id          INTEGER   PRIMARY KEY AUTOINCREMENT,
    summary     TEXT      CONSTRAINT [summary may not be empty] CHECK (LENGTH(summary) > 0) 
                          NOT NULL,
    description TEXT,
    duedate     DATE      NOT NULL
                          DEFAULT (DATE('now', 'localtime') ),
    status_id   TEXT      NOT NULL
                          REFERENCES status (id) 
                          DEFAULT O,
    modified    TIMESTAMP DEFAULT (DATETIME('now', 'localtime') ) 
);

INSERT INTO task (
                     id,
                     summary,
                     description,
                     duedate,
                     status_id,
                     modified
                 )
                 VALUES (
                     1,
                     'Read',
                     'Read something to get a good introduction into Python',
                     '2020-01-01',
                     'C',
                     '2017-09-18 09:10:20'
                 );

INSERT INTO task (
                     id,
                     summary,
                     description,
                     duedate,
                     status_id,
                     modified
                 )
                 VALUES (
                     2,
                     'Visit',
                     'Visit the python.org website',
                     '2015-03-27',
                     'C',
                     '2017-09-17 17:58:28'
                 );

INSERT INTO task (
                     id,
                     summary,
                     description,
                     duedate,
                     status_id,
                     modified
                 )
                 VALUES (
                     3,
                     'Test',
                     'Test various editors and check the syntax highlighting',
                     '2015-01-01',
                     'O',
                     '2017-09-17 17:58:40'
                 );

INSERT INTO task (
                     id,
                     summary,
                     description,
                     duedate,
                     status_id,
                     modified
                 )
                 VALUES (
                     4,
                     'Choose',
                     'Choose your favorite GUI-Framework',
                     '2015-01-03',
                     'O',
                     '2016-05-15 10:57:26'
                 );

INSERT INTO task (
                     id,
                     summary,
                     description,
                     duedate,
                     status_id,
                     modified
                 )
                 VALUES (
                     5,
                     'Duck',
                     'Go up the Amazon on a rubber duck',
                     '2015-01-01',
                     'O',
                     '2017-09-17 17:58:58'
                 );


-- Trigger: update modified
DROP TRIGGER IF EXISTS "update modified";
CREATE TRIGGER [update modified]
         AFTER UPDATE
            ON task
      FOR EACH ROW
          WHEN NEW.modified = OLD.modified
BEGIN
    UPDATE task
       SET modified = CURRENT_TIMESTAMP
     WHERE id = OLD.id;
END;


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
