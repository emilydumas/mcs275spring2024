# MCS 275 spring 2024 lecture 32
# Sample web application (task list)
# David Dumas
from flask import Flask, render_template, request
import time
import timefmt
import collections
import sqlite3

"Task list web application using sqlite"

DB_FN = "activetask.db"

ST_WAIT = 0
ST_PROGRESS = 1
ST_COMPLETE = 2

STATUS_DESC = {
    ST_WAIT: "Waiting",
    ST_PROGRESS: "In progress",
    ST_COMPLETE: "Completed",
}

SH_PRIVATE = 0
SH_SHARED = 1

SHARED_DESC = {
    SH_PRIVATE: "private",
    SH_SHARED: "shared",
}

app = Flask(__name__)


# go to /tasks/ddumas/
# then this function will be called as task_list_view(username="ddumas")
@app.route("/tasks/<username>/")
def task_list_view(username):  # Logical name for this action
    now = time.time()
    con = sqlite3.connect(DB_FN)

    this_user_results = con.execute(
        """
        SELECT taskid, description, status, shared, updated_ts
        FROM tasks
        WHERE owner=?;
        """,
        [username],
    )
    this_user_tasks = {ST_WAIT: [], ST_PROGRESS: [], ST_COMPLETE: []}
    for row in this_user_results:
        status = row[2]
        this_user_tasks[status].append(
            {
                "taskid": row[0],
                "description": row[1],
                "shared_code": row[3],
                "shared_str": SHARED_DESC[row[3]],
                "updated_ts": row[4],
                "updated_str": timefmt.ts_fmt(row[4]),
                "updated_delta_str": timefmt.tsdiff_fmt(now - row[4]),
            }
        )

    # Now, this_user_tasks is dictionary mapping status codes to lists of
    # task data dictionaries, like
    # {
    #   0: [ {"description":..., }, {"description":...,} ],
    #   1: [ {"description":..., }, {"description":...,} ],
    #   2: [ {"description":..., }, {"description":...,} ],
    #  }

    other_user_results = con.execute(
        """
        SELECT taskid, owner, description, status, updated_ts
        FROM tasks
        WHERE owner != ? AND shared=1;
        """,
        [username],
    )
    other_user_tasks = collections.defaultdict(list)
    for row in other_user_results:
        owner = row[1]
        other_user_tasks[owner].append(
            {
                "taskid": row[0],
                "description": row[2],
                "status_code": row[3],
                "status_str": STATUS_DESC[row[3]],
                "updated_ts": row[4],
                "updated_str": timefmt.ts_fmt(row[4]),
                "updated_delta_str": timefmt.tsdiff_fmt(now - row[4]),
            }
        )

    return render_template(
        "task_list_view.html",
        username=username,
        this_user_tasks=this_user_tasks,
        other_user_tasks=other_user_tasks,
        ST_WAIT=ST_WAIT,
        ST_PROGRESS=ST_PROGRESS,
        ST_COMPLETE=ST_COMPLETE,
    )


@app.route("/task/<taskid>/update")
def update(taskid):
    "Perform an update on one row to change the status (TODO: to change other things too)"
    con = sqlite3.connect(DB_FN)
    con.execute(
        "UPDATE tasks SET status=? WHERE taskid=?;",
        [int(request.values.get("status")), int(taskid)],
    )
    con.commit()
    con.close()


# Make sure we have a database, create if needed
try:
    # Do something that will only work if the tasks
    # table is present
    tstcon = sqlite3.connect(DB_FN)
    tstcon.execute("SELECT COUNT(*) FROM tasks;")
except sqlite3.OperationalError:
    print("WARNING: Database not found; creating.")
    print("(Maybe you want to run add_sample_tasks.py to add sample data?)\n")
    tstcon.execute("DROP TABLE IF EXISTS tasks;")
    tstcon.execute(
        """
        CREATE TABLE tasks (
            taskid INTEGER PRIMARY KEY,
            description TEXT NOT NULL,
            owner TEXT NOT NULL,
            status INTEGER NOT NULL DEFAULT 0,
            shared INTEGER NOT NULL DEFAULT 0,
            created_ts REAL,
            updated_ts REAL
        );"""
    )
    tstcon.commit()
finally:
    tstcon.close()

# Start the web server
app.run()
