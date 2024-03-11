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
for row in res:  # demand the results; could also fetch with res.fetchall()
    fuels.append( row[0] )

print("FUELS FOUND: {}".format(", ".join(fuels)))
print()

for f in fuels:
    print("TOP TEN {} PLANTS".format(f))
    res = con.execute("""
        SELECT capacity_mw,name,country
        FROM powerplants
        WHERE primary_fuel=?
        ORDER BY capacity_mw DESC
        LIMIT 10;
                """,  [f] )
    for row in res:
        print("{:.0f}MW: {} ({})".format(row[0],row[1],row[2]))
    print()

con.close()
