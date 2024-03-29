DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks (
    taskid INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    owner TEXT NOT NULL,
    status INTEGER NOT NULL DEFAULT 0,
    shared INTEGER NOT NULL DEFAULT 0,
    created_ts REAL NOT NULL,
    updated_ts REAL NOT NULL
);
