"Make a CSV of the UIC academic calendar"
# MCS 275 Spring 2024
# David Dumas
import bs4
import time
import urllib
import time
import os
import csv
import sys

cal_url = "https://catalog.uic.edu/ucat/academic-calendar/"
cache_fn = "uic_academic_cal.html"
target_year = "2024-2025"

if len(sys.argv)>1:
    target_year = sys.argv[1]

out_fn = "uic_academic_cal_{}.csv".format(target_year.replace("-","_"))

# Once and only once, store a local copy
if os.path.exists(cache_fn):
    print("Local copy already exists")
else:
    #download
    time.sleep(1)
    with urllib.request.urlopen(cal_url) as http_fp:
        with open(cache_fn,"wb") as local_fp:
            local_fp.write( http_fp.read() )
    print("Downloaded a local copy!")

with open(cache_fn,"rb") as fp:
    soup = bs4.BeautifulSoup(fp,"html.parser")

target_h2 = None
for tag in soup.find_all("h2"):
    s = tag.text.lower()
    if "academic calendar" in s and target_year in s:
        target_h2 = tag
        break

if target_h2 is None:
    print("ERROR: Could not find the section for year {}".format(target_year))
    exit(1)

ay_table = target_h2.find_next_sibling("table")  # first table after the h2
if ay_table is None:
    print("ERROR: Did not find expected calendar table for {}".format(target_year))
    exit(1)

with open(out_fn,"w",newline="",encoding="UTF-8") as fp:
    writer = csv.writer(fp)
    semester = None
    for row in ay_table.find_all("tr"):
        tds = row.find_all("td")
        if len(tds) != 2:
            # Row with # td tags != 2 is not relevant
            continue
        if not tds[1].text.strip():
            # Semester heading rows have only one nonempty td
            semester = tds[0].text.replace("\n"," ").strip()
        else:
            # Ordinary schedule item is: date event
            if semester is not None:
                date = tds[0].text.replace("\n"," ").strip()
                event = tds[1].text.replace("\n"," ").strip()
                writer.writerow([semester,date,event])

print("Wrote",out_fn)