"""
Generate tiny sqlite database of planet data
more complete than the one we'll prepare live
in lecture 27.
"""

# Note: All the "IF NOT EXISTS" in these SQL commands make it
# so the program won't raise an exception if the database file
# already exists.
import sqlite3

con = sqlite3.connect("solarsystem.sqlite")  # .db also popular
con.execute(
    """CREATE TABLE IF NOT EXISTS planets (
            planet_id INTEGER PRIMARY KEY,
            name TEXT,
            radius_au REAL, 
            year_discovered INTEGER
        );"""
)
con.execute(
    """CREATE TABLE IF NOT EXISTS moons (
            moon_id INTEGER PRIMARY KEY,
            parent INTEGER,
            name TEXT,
            radius_km REAL, 
            year_discovered INTEGER
        );"""
)
# In case the table already exists, delete all its rows.
con.execute("DELETE FROM planets;")
con.execute("DELETE FROM moons;")

# List of tuples to add
planetdata = [
    (1, "Mercury", 0.4, None),
    (2, "Venus", 0.7, None),
    (3, "Earth", 1.0, None),
    (4, "Mars", 1.5, None),
    (5, "Jupiter", 5.2, None),
    (6, "Saturn", 9.5, None),
    (7, "Uranus", 19.2, 1781),
    (8, "Neptune", 30.1, 1846),
]

# Loop to add each tuple as a row of the table
for row in planetdata:
    con.execute("INSERT INTO planets VALUES (?,?,?,?);", row)

moondata = [
    (1, 3, "Moon", 384399, None),
    (2, 4, "Phobos", 9380, 1877),
    (3, 4, "Deimos", 23460, 1877),
    (4, 5, "Io", 421800, 1610),
    (5, 5, "Europa", 671100, 1610),
    (6, 5, "Ganymede", 1070400, 1610),
    (7, 5, "Callisto", 1882700, 1610),
    (8, 6, "Mimas", 185540, 1789),
    (9, 6, "Enceladus", 238040, 1789),
    (10, 6, "Tethys", 294670, 1684),
    (11, 6, "Dione", 2377420, 1684),
    (12, 6, "Rhea", 527070, 1672),
    (13, 6, "Titan", 1221870, 1655),
    (14, 6, "Hyperion", 1500880, 1848),
    (15, 6, "Iapetus", 3560840, 1671),
    (16, 6, "Phoebe", 12947780, 1898),
    (17, 7, "Ariel", 190900, 1851),
    (18, 7, "Umbriel", 266000, 1851),
    (19, 7, "Titania", 436300, 1787),
    (20, 7, "Oberon", 583500, 1787),
    (21, 7, "Miranda", 129900, 1949),
    (22, 8, "Triton", 354800, 1846),
]


# Loop to add each tuple as a row of the table
for row in moondata:
    con.execute("INSERT INTO moons VALUES (?,?,?,?,?);", row)

con.commit()  # Save any changes to disk
con.close()  # Close the database file
