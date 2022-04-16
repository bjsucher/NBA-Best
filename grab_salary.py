import sqlite3
import os

con = sqlite3.connect(
    "C:/Users/brand/OneDrive - Duke University/BIOS_821/NBA-Best/nba.db"
)

cur = con.cursor()

# nba_table = cur.execute("SELECT * FROM Salary")
# for row in nba_table:
#     print(row)

# query = "SELECT * FROM Salary WHERE Name = " + "'Stephen Curry'"
# query = "SELECT * FROM Salary"
# query = (
#     "SELECT tableName FROM sqlite_master WHERE type = 'table' AND tableName = 'Salary'"
# )
# query = "SELECT * FROM sqlite_master"
query = "SELECT * FROM PlayerStats"
is_in_table = cur.execute(query)
for row in is_in_table:
    print(row)
