"Add a few sample rows to the database"
import sqlite3
import sys
import time
import random

DB_FN = "activetask.db"

users = ["ddumas", "vjones"]

descriptions = [
    "Complete Python homework",
    "Read chapter 4 of algorithms textbook",
    "Attend MCS 275 study group on Wednesday",
    "Submit project proposal by Friday",
    "Review readings for art history exam",
    "Practice coding problems before interview",
    "Update resume with new skills",
    "Email professor about office hours",
    "Plan project timeline with team",
    "Study for upcoming midterm exam",
    "Fix bugs in personal project code",
    "Attend colloquium lecture on machine learning",
    "Watch tutorial on web development basics",
    "Attend MCS 275 lab",
    "Prepare presentation for German class",
    "Join online forum about card games",
    "Research summer internships",
    "Back up all school work to cloud storage",
    "Organize study materials in folders",
    "Meet with advisor to discuss course selection",
    "Volunteer for student recruiting event",
    "Review privacy of social media profiles",
    "Schedule meeting with project group",
    "Learn basics of Haskell and Julia",
    "Write a blog post about recent tech news",
    "Clean up and comment code in repository",
    "Review notes from last class",
    "Repair lock on velociraptor cage",
    "Set up a study schedule in preparation for finals week",
]

try:
    # Do something that will only work if the tasks
    # table is present
    con = sqlite3.connect(DB_FN)
    con.execute("SELECT COUNT(*) FROM tasks;")
except sqlite3.OperationalError:
    print("WARNING: Database not found; creating.")
    con.execute("DROP TABLE IF EXISTS tasks;")
    con.execute(
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
    con.commit()

random.shuffle(descriptions)
for d in descriptions[:5]:
    res = con.execute("SELECT COUNT(*) FROM tasks WHERE description=?;", [d])
    if res.fetchone()[0]:
        print("Not adding task '{}': Already a task with that description.".format(d))
        continue
    u = random.choice(users)
    elapsed = 3600.0 * (1 + 24 * 365 * random.random())
    con.execute(
        """
        INSERT INTO tasks (description, owner, status, shared, created_ts, updated_ts)
        VALUES (?, ?, ?, ?, ?, ?);""",
        [
            d,
            u,
            random.randrange(3),
            random.randrange(2),
            time.time() - elapsed,
            time.time() - elapsed,
        ],
    )
    print("Added a task for user '{}'".format(u))
con.commit()
con.close()
