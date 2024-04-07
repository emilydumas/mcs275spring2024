# MCS 275 spring 2024 lecture 32-34
# Sample web application (task list)
# David Dumas
from flask import Flask, render_template, request, redirect, abort
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
    SH_PRIVATE: "Private",
    SH_SHARED: "Shared",
}

UPDATABLE_COLS = ["status", "shared"]

app = Flask(__name__)


@app.route("/")
def front():
    "Front page"
    # if a query parameter `fail` is given, then
    # the template will show an error message too.
    return render_template("front.html", fail=request.values.get("fail"))


@app.route("/login", methods=["GET", "POST"])
def login():
    "Login action: sends user to task view"
    username = request.values.get("username")
    if username is None or (not username.strip()):
        return redirect("/?fail=1", code=302)
    return redirect("/tasks/{}/".format(username), code=302)


# go to /tasks/ddumas/
# then this function will be called as task_list_view(username="ddumas")
@app.route("/tasks/<username>/")
def task_list_view(username):  # Logical name for this action
    "View of one user's owned tasks and all public ones"
    show_completed = ("show_completed" in request.values) and (
        request.values.get("show_completed") == "1"
    )
    now = time.time()
    con = sqlite3.connect(DB_FN)

    this_user_results = con.execute(
        """
        SELECT taskid, description, status, shared, updated_ts
        FROM tasks
        WHERE owner=?
        ORDER BY created_ts DESC;
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
        WHERE owner != ? AND shared=1
        ORDER BY created_ts DESC;
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
        show_completed=show_completed,
    )


def update_query_builder(params):
    """
    Convert dictionary like {"status":1, "shared":0} to a SQL SET
    clause like 'status=? AND shared=?' and a list of arguments like
    [1,0].
    """
    if not params:
        raise ValueError("No columns to update.")
    placeholders = []
    args = []
    for k in params:
        if k not in UPDATABLE_COLS:
            raise ValueError("Column name '{}' not known or not allowed.".format(k))
        placeholders.append("{}=?".format(k))
        args.append(int(params[k]))
    return ", ".join(placeholders), args


@app.route("/task/<int:taskid>/update")
def update(taskid):
    "Perform an update on one row to change the status (TODO: to change other things too)"
    con = sqlite3.connect(DB_FN)
    query_params = dict(request.values)  # convert query params to a dict
    username = query_params.pop("username")
    try:
        set_clause, set_args = update_query_builder(query_params)
    except ValueError:
        abort(400)  # tells Flask to return 400 BAD REQUEST
    # Make the full query, which also always updates the timestamp
    query = "UPDATE tasks SET " + set_clause + ", updated_ts=? WHERE taskid=?;"
    print("Using query '{}'".format(query))
    con.execute(
        query,
        set_args + [time.time(), taskid],
    )
    con.commit()
    con.close()
    return redirect("/tasks/{}/".format(username), code=302)


@app.route("/task/new/")
def add_task_form():
    "Display the form to create a new task"
    return render_template("add_task.html")  # will submit data to /task/new/submit


@app.route("/task/new/submit", methods=["GET", "POST"])
def add_task():
    "Process form submission"
    now = time.time()
    con = sqlite3.connect(DB_FN)
    con.execute(
        """
                INSERT INTO tasks (description,owner,created_ts,updated_ts)
                VALUES (?,?,?,?);
                """,
        [request.values.get("description"), request.values.get("owner"), now, now],
    )
    con.commit()
    con.close()
    return redirect("/task/new/", code=302)


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
