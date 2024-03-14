# MCS 275 Spring 2024 Lecture 28
# David Dumas
"Task list manager using SQLite for storage"

import sqlite3
import sys


def get_db_connection():
    con = sqlite3.connect("tasks.db")
    # any verification or initialization can go here
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
        print("Unknown flag '{}'".format(flag))
        exit(1)
        
    for taskid, desc, complete in res:
        if complete:
            donechar = "\u2713"
        else:
            donechar = " "
        print("{}{:3d} {}".format(donechar, taskid, desc))
    con.close()


def do_done(taskid_str):
    taskid = int(taskid_str)
    con = get_db_connection()
    con.execute(
        """
        UPDATE tasks SET complete=1 WHERE id=?;
                """,
        [taskid],
    )
    con.commit()
    con.close()


def do_delete(taskid_str):
    taskid = int(taskid_str)
    con = get_db_connection()
    res = con.execute(
        """
        DELETE FROM tasks WHERE id=?;
                """,
        [taskid],
    )
    if res.rowcount == 0:
        print("WARNING: No such task")
        exit(1)
    con.commit()
    con.close()


if __name__ == "__main__":
    # sys.argv[0] is the name of this script
    # sys.argv[1] is the first command line argument
    # ...
    command = sys.argv[1]  # e.g. "add", "list", "delete"
    operand = None
    if len(sys.argv) > 2:
        operand = sys.argv[2]  # data used by the command, e.g. task description

    if command == "add":
        do_add(operand)
    elif command == "list":
        do_list(operand)
    elif command == "done":
        do_done(operand)
    elif command == "delete":
        do_delete(operand)
    else:
        print("Unknown command")
        exit(1)
