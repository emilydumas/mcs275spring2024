# MCS 275 Spring 2024 lecture 32
# Sample web application
# David Dumas
from flask import Flask, render_template, request
import time
import sqlite3

"Task list manager web application using SQLite"

DB_FN = "taskgain.db"

STATUS_DESC = {
    0: "Waiting",
    1: "In progress",
    2: "Completed",
}

SHARED_DESC = {
    0: "private",
    1: "shared",
}

# Make a new Flask object, which represents our web server
app = Flask(__name__)


@app.route("/task/<taskid>/update")
def update_task(taskid):
    con = sqlite3.connect(DB_FN)
    con.execute(
        "UPDATE tasks SET status=? WHERE taskid=?",
        [int(request.values.get("status")), int(taskid)],
    )
    # if status=0 is at the end of the URL, this returns "0"
    con.commit()
    con.close()


@app.route("/tasks/<username>/")
def task_list_view(username):
    con = sqlite3.connect(DB_FN)
    this_user_results = con.execute(
        """
        SELECT taskid, description, status, shared, updated_ts
        FROM tasks
        WHERE owner=?;
        """,
        [username],
    )
    this_user_tasks = []
    for row in this_user_results:
        this_user_tasks.append(
            {
                "taskid": row[0],
                "description": row[1],
                "status": row[2],
                "shared": row[3],
                "updated_ts": row[4],
            }
        )
    # Now, this_user_tasks is a list of dictionaries
    return render_template(
        "task_list_view.html",
        username=username,
        this_user_tasks=this_user_tasks,
        STATUS_DESC=STATUS_DESC,
        SHARED_DESC=SHARED_DESC,
    )


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
            created_ts REAL NOT NULL,
            updated_ts REAL NOT NULL
        );"""
    )
    tstcon.commit()
finally:
    tstcon.close()

app.run()
# never returns
