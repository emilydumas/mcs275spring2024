# MCS 275 spring 2024 lecture 32
# Sample web application (task list)
# David Dumas
from flask import Flask, render_template, request
import time
import sqlite3

"Task list web application using sqlite"

DB_FN = "activetask.db"

STATUS_VALS = {
    0: "Waiting",
    1: "In progress",
    2: "Completed",
}

SHARED_VALS = {
    0: "Private",
    1: "Shared",
}

app = Flask(__name__)


# go to /tasks/ddumas/
# then this function will be called as task_list_view(username="ddumas")
@app.route("/tasks/<username>/")
def task_list_view(username):  # Logical name for this action
    "Show the tasks for the current user and public tasks of others"
    con = sqlite3.connect(DB_FN)
    this_user_results = con.execute(
        """
        SELECT taskid, description, status, shared, updated_ts
        FROM tasks
        WHERE owner=?;                                
    """,
        [username],
    )
    this_user_rows = []  # list of dictionaries with info about this user's tasks
    for row in this_user_results:
        this_user_rows.append(
            {
                "taskid": row[0],
                "description": row[1],
                "status": row[2],
                "shared": row[3],
                "updated_ts": row[4],
            }
        )
    con.close()
    # Send this_user_rows off to the template and render it
    return render_template(
        "task_list_view.html",
        this_user_rows=this_user_rows,
        username=username,
        STATUS_VALS=STATUS_VALS,
        SHARED_VALS=SHARED_VALS,
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
