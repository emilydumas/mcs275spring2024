# MCS 275 Spring 2024 Lecture 28
# Emily Dumas
"Task list manager using SQLite for storage"

import sqlite3
import sys
import os

# Add path here if needed
DB_FILENAME = "tasks.db"

SQL_TABLE_CREATE = """
CREATE TABLE IF NOT EXISTS tasks (
id INTEGER PRIMARY KEY,
desc TEXT,
complete INTEGER DEFAULT 0 );
"""


def ensure_table_exists(con):
    "Use cursor `con` to make the table we need (do nothing if it exists)"
    con.execute(SQL_TABLE_CREATE)
    con.commit()


def create_db_and_table():
    "Assuming database file does not exist, create it and the table we need"
    assert not os.path.exists(DB_FILENAME)
    con = sqlite3.connect(DB_FILENAME)
    ensure_table_exists(con)
    return con


def get_db_connection():
    if not os.path.exists(DB_FILENAME):
        print("WARNING: The database file '{}' was not found.".format(DB_FILENAME))
        print("The current working directory is '{}'.".format(os.getcwd()))
        print("Create and initialize new database? Y/N")
        sel = None
        while sel not in ("Y", "N"):
            sel = input().upper()
        if sel == "N":
            print("Exiting.")
            exit()
        con = create_db_and_table()
        print("OK, created database.\n")
        return con

    con = sqlite3.connect(DB_FILENAME)
    ensure_table_exists(con)
    return con


def do_add(c, description):
    c.execute(
        """
        INSERT INTO tasks (desc)
        VALUES (?);
                """,
        [description],
    )


def do_list(c, flag):
    if flag == None:
        res = c.execute(
            """
            SELECT id,desc,complete FROM tasks WHERE complete=0;
                    """
        )
    elif flag == "all":
        res = c.execute(
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


def do_done(c, taskid_str):
    taskid = int(taskid_str)
    c.execute(
        """
        UPDATE tasks SET complete=1 WHERE id=?;
                """,
        [taskid],
    )


def do_undo(c, taskid_str):
    taskid = int(taskid_str)
    c.execute(
        """
        UPDATE tasks SET complete=0 WHERE id=?;
                """,
        [taskid],
    )


def do_delete(c, taskid_str):
    taskid = int(taskid_str)
    res = c.execute(
        """
        DELETE FROM tasks WHERE id=?;
                """,
        [taskid],
    )
    if res.rowcount == 0:
        print("WARNING: No such task")
        exit(1)


def do_reset(c):
    print("This will remove ALL tasks from the database.")
    print("Are you sure? (Y to proceed)")
    s = input()
    if s.upper() != "Y":
        print("Action aborted.")
        exit()
    c.execute("DELETE FROM tasks;")
    print("OK, all tasks deleted.")


def usage():
    print("Specify a task management command as the first command line argument")
    print("e.g.")
    print('  add "Do laundry" - add a task with given description')
    print("  list - show incomplete tasks")
    print("  list all - show all tasks (including completed ones)")
    print("  done 15 - complete the task with id 15")
    print("  undo 15 - mark the task with id 15 as incomplete")
    print("  delete 15 - delete the task with id 15")
    print("  reset - delete all tasks")


if __name__ == "__main__":
    # sys.argv[0] is the name of this script
    # sys.argv[1] is the first command line argument
    # ...
    command = None
    if len(sys.argv) > 1:
        command = sys.argv[1]  # e.g. "add", "list", "delete"
    operand = None
    if len(sys.argv) > 2:
        operand = sys.argv[2]  # data used by the command, e.g. task description

    con = get_db_connection()
    with con:  # will auto commit() at end of block
        if command == None:
            usage()
        elif command == "add":
            do_add(con, operand)
        elif command == "list":
            do_list(con, operand)
        elif command == "done":
            do_done(con, operand)
        elif command == "undo":
            do_undo(con, operand)
        elif command == "delete":
            do_delete(con, operand)
        elif command == "reset":
            do_reset(con)
        else:
            print("Unknown command")
            exit(1)
    con.close()
