# MCS 275 Spring 2024 Lecture 27
"Manage a list of tasks stored in a SQLite database"

import sqlite3
import sys


def get_db_connection():
    con = sqlite3.connect("tasks.db")
    # Verify the necessary tables are there
    return con


def do_add(description):
    con = get_db_connection()
    con.execute(
        """
        INSERT INTO tasks (desc)
        VALUES (?);
                """,
        [description],
    )
    con.commit()
    con.close()


def do_list(flag):
    con = get_db_connection()
    if flag == None:
        res = con.execute(
            """
            SELECT id,desc,complete FROM tasks WHERE complete=0; 
                    """
        )
    elif flag == "all":
        res = con.execute(
            """
            SELECT id,desc,complete FROM tasks; 
                    """
        )
    else:
        print("Unknown directive '{}'".format(flag))
        exit(1)

    for taskid, desc, complete in res:
        if complete:
            donechar = "\u2713"  # Check mark
        else:
            donechar = " "
        print("{} {:3d} {}".format(donechar, taskid, desc))
    con.close()


def do_done(taskid_str):
    taskid = int(taskid_str)
    con = get_db_connection()
    res = con.execute(
        """
        UPDATE tasks
        SET complete=1
        WHERE id=?;
                """,
        [taskid],
    )
    if res.rowcount == 0:
        print("No such task!")
        exit(1)
    con.commit()
    con.close()


def do_delete(taskid_str):
    taskid = int(taskid_str)
    con = get_db_connection()
    con.execute(
        """
        DELETE FROM tasks
        WHERE id=?;
                """,
        [taskid],
    )
    con.commit()
    con.close()


# table tasks
# CREATE TABLE tasks (
# id INTEGER PRIMARY KEY,
#   ...> desc TEXT,
#   ...> complete INTEGER DEFAULT 0 );

if __name__ == "__main__":
    # process command line arguments
    # sys.argv[0] is the name of this Python script
    # sys.argv[1] is the first argument e.g. "add"
    # sys.argv[2] is the next, e.g. "fold the laundry"
    command = sys.argv[1]
    if len(sys.argv) > 2:
        operand = sys.argv[2]
    else:
        operand = None

    if command == "add":
        do_add(operand)
    elif command == "list":
        do_list(operand)  # None or "all"
    elif command == "done":
        do_done(operand)  # task id
    elif command == "delete":
        do_delete(operand)  # task id
    else:
        print("Unknown command!")
        exit(1)
