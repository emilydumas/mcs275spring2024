# MCS 275 Spring 2024 Lecture 27
# David Dumas
"Query the powerplants database and print some info"

import sqlite3

# Need powerplants.sqlite from:
# https://www.dumas.io/teaching/2024/spring/mcs275/data/powerplants.sqlite
con = sqlite3.connect("powerplants.sqlite")

res = con.execute("SELECT DISTINCT primary_fuel FROM powerplants;")
# res is a promise to give us the rows ON REQUEST

fuels = []
for row in res: # request the rows, one by one
    fuels.append(row[0])  #row[0] means "first column returned"

# fuels = [ row[0] for row in res ]

for fuel in fuels:
    print("TOP TEN WITH FUEL =",fuel)
    res = con.execute("""
                SELECT country,name
                FROM powerplants
                WHERE primary_fuel=?
                ORDER BY capacity_mw
                DESC LIMIT 10;
                """, (fuel,) )
    print(res.fetchall())

con.close()
