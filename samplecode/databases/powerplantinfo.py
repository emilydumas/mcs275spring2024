# MCS 275 Spring 2024 Lecture 27
# David Dumas
"List top ten power plants for each fuel"

import sqlite3

# Need to download sqlite file from:
# https://www.dumas.io/teaching/2024/spring/mcs275/data/powerplants.sqlite
con = sqlite3.connect("powerplants.sqlite")

res = con.execute("SELECT DISTINCT primary_fuel FROM powerplants;")
# res is basically a promise to produce results on demand

fuels = []
for row in res:
    fuels.append( row[0] )

print("FUELS FOUND:",fuels)

for f in fuels:
    print("TOP TEN {} PLANTS".format(f))
    res = con.execute("""
        SELECT name,capacity_mw
        FROM powerplants
        WHERE primary_fuel=?
        ORDER BY capacity_mw DESC
        LIMIT 10;
                """,  [f] )
    for row in res:
        print(row[0],row[1])  # row[0] is name row[1] is capacity_mw
    print()

con.close()