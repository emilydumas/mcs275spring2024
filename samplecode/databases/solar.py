# SQLite first example
# MCS 275 Spring 2024 Lecture 26
# Emily Dumas
"Create a database, table, and some rows.  Read them back."

import sqlite3

# Create or open the database
con = sqlite3.connect("solarsystem.sqlite")  # .db also popular

# Create the table

con.execute(
    """
    CREATE TABLE IF NOT EXISTS planets (
            planet_id INTEGER PRIMARY KEY,
            name TEXT,
            radius_au REAL,
            year INTEGER
    );
"""
)

# If the table already exists, it might have content
# Clear all rows
con.execute("DELETE FROM planets;")

# Add data
con.execute(
    """
INSERT INTO planets VALUES (?,?,?,?);
""",
    (3, "Earth", 1.0, None),
)

con.execute(
    """
INSERT INTO planets VALUES (?,?,?,?);
""",
    (8, "Neptune", 30.1, 1846),
)

# Commit the changes
con.commit()  # only needed because we wrote new data


# TODO: Read data it back


# Close connection (i.e. also close the file)
con.close()
