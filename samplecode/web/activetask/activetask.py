# MCS 275 spring 2024 lecture 32-34
# Sample web application (task list)
# David Dumas
from flask import Flask, render_template, request, redirect, abort
import time
import timefmt
import collections
import sqlite3
import datetime

"Task list web application using sqlite"
__version__ = "1.2"
# Versions:
#   1.0 last lecture demo
#   1.1 with worksheet 13 solution
#   1.2 with homework 13 solution

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


def timestamp_range_for_day(year, month, day):
    """
    Return the timestamps when a calendar day
    begins and ends.
    """
    ts0 = datetime.datetime(year, month, day).timestamp()
    ts1 = (datetime.datetime(year, month, day) + datetime.timedelta(days=1)).timestamp()
    return ts0, ts1


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


@app.route("/audit/troubled/")
def troubled_task_audit():
    "Show troubled tasks"
    now = time.time()
    week_ago = now - 7 * 24 * 60 * 60
    con = sqlite3.connect(DB_FN)

    stale_results = con.execute(
        """
        SELECT taskid, description, owner, status, shared, updated_ts
        FROM tasks
        WHERE status = ? AND created_ts <= ?
        ORDER BY created_ts DESC;
        """,
        [ST_WAIT, week_ago],
    )
    stale_tasks = []
    for row in stale_results:
        stale_tasks.append(
            {
                "taskid": row[0],
                "description": row[1],
                "owner": row[2],
                "status": row[3],
                "status_str": STATUS_DESC[row[3]],
                "shared_code": row[4],
                "shared_str": SHARED_DESC[row[4]],
                "updated_ts": row[5],
                "updated_str": timefmt.ts_fmt(row[5]),
                "updated_delta_str": timefmt.tsdiff_fmt(now - row[5]),
            }
        )

    lrt_results = con.execute(
        """
        SELECT taskid, description, owner, status, shared, updated_ts
        FROM tasks
        WHERE status = ? AND updated_ts <= ?
        ORDER BY created_ts DESC;
        """,
        [ST_PROGRESS, week_ago],
    )
    lrt_tasks = []
    for row in lrt_results:
        lrt_tasks.append(
            {
                "taskid": row[0],
                "description": row[1],
                "owner": row[2],
                "status": row[3],
                "status_str": STATUS_DESC[row[3]],
                "shared_code": row[4],
                "shared_str": SHARED_DESC[row[4]],
                "updated_ts": row[5],
                "updated_str": timefmt.ts_fmt(row[5]),
                "updated_delta_str": timefmt.tsdiff_fmt(now - row[5]),
            }
        )
    return render_template(
        "troubled_task_audit.html",
        stale_tasks=stale_tasks,
        lrt_tasks=lrt_tasks,
    )


@app.route("/task/<int:taskid>/")
def single_task_view(taskid):
    "Display data about one task"
    con = sqlite3.connect(DB_FN)
    taskdata = con.execute(
        """
        SELECT description, owner, status, shared, updated_ts, created_ts
        FROM tasks
        WHERE taskid=?;
        """,
        [taskid],
    ).fetchone()
    con.close()

    if taskdata is None:
        # No row returned => taskid does not exist
        # NOTE: worksheet said to return 400, but
        # really a 404 would be more appropriate!
        abort(400)

    return render_template(
        "single_task_view.html",
        taskid=taskid,
        description=taskdata[0],
        owner=taskdata[1],
        status=taskdata[2],
        status_str=STATUS_DESC[taskdata[2]],
        shared=taskdata[3],
        shared_str=SHARED_DESC[taskdata[3]],
        updated_ts=taskdata[4],
        updated_str=timefmt.ts_fmt(taskdata[4]),
        created_ts=taskdata[5],
        created_str=timefmt.ts_fmt(taskdata[5]),
    )


@app.route("/reports/day/<int:year>/<int:month>/<int:day>/")
def on_this_day(year, month, day):
    "View tasks created or updated on a certain day"
    now = time.time()
    ts0, ts1 = timestamp_range_for_day(year, month, day)
    con = sqlite3.connect(DB_FN)

    created_results = con.execute(
        """
        SELECT taskid, description, owner, status, shared, updated_ts
        FROM tasks
        WHERE created_ts >= ? AND created_ts < ?
        ORDER BY created_ts DESC;
        """,
        [ts0, ts1],
    )
    created_tasks = []
    for row in created_results:
        created_tasks.append(
            {
                "taskid": row[0],
                "description": row[1],
                "owner": row[2],
                "status": row[3],
                "status_str": STATUS_DESC[row[3]],
                "shared_code": row[4],
                "shared_str": SHARED_DESC[row[4]],
                "updated_ts": row[5],
                "updated_str": timefmt.ts_fmt(row[5]),
                "updated_delta_str": timefmt.tsdiff_fmt(now - row[5]),
            }
        )
    updated_results = con.execute(
        """
        SELECT taskid, description, owner, status, shared, updated_ts
        FROM tasks
        WHERE updated_ts >= ? AND updated_ts < ?
        ORDER BY created_ts DESC;
        """,
        [ts0, ts1],
    )
    updated_tasks = []
    for row in updated_results:
        updated_tasks.append(
            {
                "taskid": row[0],
                "description": row[1],
                "owner": row[2],
                "status": row[3],
                "status_str": STATUS_DESC[row[3]],
                "shared_code": row[4],
                "shared_str": SHARED_DESC[row[4]],
                "updated_ts": row[5],
                "updated_str": timefmt.ts_fmt(row[5]),
                "updated_delta_str": timefmt.tsdiff_fmt(now - row[5]),
            }
        )

    return render_template(
        "on_this_day_view.html",
        year="{:04d}".format(year),
        month="{:02d}".format(month),
        day="{:02d}".format(day),
        created_tasks=created_tasks,
        updated_tasks=updated_tasks,
    )


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
    taskid = con.execute("SELECT last_insert_rowid();").fetchone()[0]
    con.commit()
    con.close()
    return redirect("/task/{}/".format(taskid), code=302)


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
